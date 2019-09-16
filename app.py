# coding:utf-8
from flask import Flask, render_template, session, jsonify
import time
import requests
import re
from xml_parser import xml_parse

app = Flask(__name__)
app.secret_key = 'thanlon'
app.debug = True


@app.route('/login')
def login():
    '''
    python的时间戳：
     In [1]: import time
     In [2]: time.time()
     Out[2]: 1566619808.3663833
     微信的时间戳：1566619911202
    '''
    ctime = int(time.time() * 1000)
    qcode_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}'.format(
        ctime)
    rep = requests.get(
        url=qcode_url,
    )
    # print(rep.text)
    qcode = re.findall('uuid = "(.*)";', rep.text)[0]
    session['qcode'] = qcode  # 下面的请求还需要用到，所以将qcode放到session中
    # print(qcode)
    return render_template('login.html', qcode=qcode)


@app.route('/check/login')
def check_login():
    'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=wbu5Y3nJLQ==&tip=1&r=-928058688&_=1568591121291'
    qcode = session['qcode']
    ctime = ctime = int(time.time() * 1000)
    check_login_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=1&r=-928058688&_={1}'.format(
        qcode, ctime)
    rep = requests.get(
        url=check_login_url,
    )
    print(rep.text)  # window.code=408;未扫码
    # 扫码后未确认登录
    # window.code=201;window.userAvatar = 'data:img/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCACEAIQDASIAAhEBAxEB/8QAHgAAAQQDAQEBAAAAAAAAAAAAAAEHCAkCAwYFBAr/xAA8EAABAwMDAgMGAgkDBQEAAAABAgMEAAURBhIhBzEIE0EJFCIyUWEVgRYjQlJicZGhwSVysSRDosLR8f/EABcBAQEBAQAAAAAAAAAAAAAAAAACAQP/xAAcEQEBAQEAAwEBAAAAAAAAAAAAARExAiFBEmH/2gAMAwEAAhEDEQA/ALU6KKKAoopNwzj1oA9jXAWpz3HqnqWF8jc23w56R+84FPNOH8koZrv6brXNwh6Y19Yb5NeREhfhs+K++6sIbSB5TwKiTgYDLnf6isrKpC8XWn0ad6760jIU6sKuC3lOKG1ClLUokpT6c5GPTB75plCPQ4qX+veicrrL1Z1LrG8OuWixz57j0aK2B7y62VHbuzwgEfYn7c108Lo1oXTURpDGnYr7pTgOy0h5wn1PxkgVzcUFdgSoYIxSg579vvU7X2NP2lYbT7hEbSMbQlpvGe3H5V8qrHpS/Mlu4Qbdcge5KULKT9vX/wDawQbyQrntXddDtGva+6s6WsDKT5k+4MMD4N4CS4NxI+gTuNPNrPw86PuDzjtquJ0+5wEpccS4zuI7EKVkfkfyo8Mmh7x0s8QlpnTI7cyPDiS5zMuMA8y4lllbpUDn4SPL9eQSOCKC5LoQyhPS+0SWytTU8vXFCnCdxS+6t5JOeezgpwK8HQlpFg0VYbYBj3KAxHx/sbSn/Fe9XWcdpwUhUB6V5OpdT2zSNnl3a83CPa7ZEbLsiZLcDbTSB3KlHgVGHTfivm+JS93e09IEyFxbc6WFXt5gIaCsAh1fmIUA1ycIA8xeP2ACaW6W4lcv5vSisRu2p3/NjnFFa19NFFFAh7VoXuSvdX0VisZTjvQN91T666Q6OWtUrUlyRHX5ZdTGSpPmFGcbjkhKE543LKU5IGckCq4/FZ7RewdTLbAtmnreXE2+f722tIUtD2G3EALUvZtPx7sBDgylJCuKbv2iVp1EjxS6ib1VJkfoyltmZbgCdjrSm8DaPUpUlxBxz8Pcbt1R56e6Bkap6mdPrVdJDNkg6kuUVpt1soJjtLkBoLUg52k4JSF8qGFHIIJ5265W76dVJ8QOt7xHlPoEZmGGlvp95f8AKWEpUEnYUKbKyCoDABPfjg48nWWvOoWn2bam5TWlM3G3M3NkqYbkhLLuQnKnEqKTkEEZ4NTD6jeHHT0vRjn6JR1yYl5LllsIuMlLsqYlh9Tci5L/AFZSlsKc3gNN7yhPmFaScV7GgfAZHv2mW4+qtMR4OposJUWTFt7S4yZzTaQy9gFRR56FCPIaeSQh0qwtKcrxKcQE0/rrX9+uke0WXUl3ZkSVKSzDgzFx0LXgnYlDZAyrGAMckgVhHtmqrzpqZqRF4ffSwQ4829cCmQpoqKfNSFKy4ApJSoJyU/CSMKAr1Lt0r1XpWd+kOlrJqt+2WdaXV35dmdZajyWVfGpLgyNqVp4UraeOUgipJ9FfD3b9YeGK76kl6wkaR1NFvphLYciiMmG/JLTTRdcQ37wtC0uowN4bSFKVg7SCEY7jElWbRVn1ZZNZuOSJDio863CYWZsR9OSFBIVlbSgMhY5SThQ+Uq+Nvq1rG3uKafvDkp1JILk5tuS4M8HDiwVAEccK5Bqe2nfZ4xNI9KdPy79qyTaL7qMKttxjutNFbTsoFLTCE7VeaQsIC0nnOVpWgo5h91w6HXDoxeLRAuenpEJ5Vsivz/MUpxDL6miFALwBhe3zMd0qK0c7CaCS/hj9p1q20atttl18tm42CQtLS5TilF1n+ILUSonucKKgcADbnNT78RXjA6f+G/TaJuoLiJt2kteZBssFQXJlA9lY7IR/GrA74yeKon6eaBvnU3VcKw6dtkq7XCQr4Y8RBWsj/H8zgDuSBki2HwvezkgaVusfXXV2QNZa2WUutwpDhfiQSANgJVy8tIAAKvhGOAcBVVN+Llvw3WluknWT2hl9i6n6pS5Og+kqXA/b9OwyUOS0fsqSk8nI/wC84PrsSAebA+nHTDTPSfSsPTulLRHs1oiDDceOnGT6qUe6lH1Uokn1NdQhtKEgJGAOABWdXJipMaF/NRQv5qK1TfRRRQFFFFBHbxmeGS09fell/UiC29q6LCKrTMUTvZWglRQnHo4CUkcg/Ce6QRCW1eDmEX4zNzDzt1vpnR2Zttkk/h8q1SUtJUy0Up8ze0lZ2KO7HyDKcKtgcAKTmo9650La7FrOWL6lQ0je5SZjL3mFCI89WxLsdSwR5aX1NsOIVkDzUKBOVpCotc/KOFtmmLRrrpX0hvlpcnw7npWOthpcAOBDhKDHltpdDTgB3tnhQ5AIynduDm6ft8LTU5nVz717n3VFvFlhQ7qp3z5Di1pWUp3hIJJbbyoNgDatSlKHKfB6QNN2HU146eWW+SNPQYw/FoFudtzbckMvKJfTladpUl8rJISRtdbIJzmnntOioFquS7m45IuNzUkp98mulxaEnulCeEtg4GQhKQcDOKyQk328GK5p/Xlm1No9cB5u3ve9wZCHRhEtKiUyFNqycgLcUk5wQoHjBBPD6Xslt1Zoq6dNtZW2P+ksaA3bZBkMpSi6MM593lslSSlQ5CiAD5ayQRwCXCjLbt93nSLJpqa7JkLIdkOkR2N2cqIC1ZGTyVIQQo85NfTJtFx1MtqPfrJZFW5K96kLdVLUSAcbQptASc+uT/mqxWGutHTtenn4827acbl/hryp0Z94MsMNyMqUZDrzkp5e7KiStKQfUg4ADaamlReqHV52XeYmmpkS2QWJcaPqN4MxnVth9LDyGlfEsKU9NxuAG0MueqQZNSdFaS0/HducyDGRHhoL6npzhcbjpSMlY3khAAGcjGMU0TGrWERbsqZaYc/Veo3k3OHp2A6XZ8pCSBF97G0CO0ltLIWVZSDvyrnaZsxFmOj6YaFsdn636qu1is1rtm+zW6JchBitskTNz7pSdnAV5bjRUMnILffFPiBiuQ6W6IVobSrUWU+Jl3lOLm3OaBj3mW4dzqwPROTtSP2UJSn0rsKucXJkFFFFapoX81FC/mooN9FFFAUUUUCEZrzbzYYV/tkq3XGMzNgSm1MvxpCAttxChgpUk8EEV6dYqIxQRyv/AIUZrTMBOkOo9+0+bZK97tjdzCboiAvkFLSnCl4NlJKC2XSgpOCmu4t3VV3SM6NYuoYjWWe6oMxL0g7LbclY7IUonyXDjPkuHP7qnMEhtPFN46dFeHVDlnYcb1Jrd0AM2WO6EpYJ7KkOdm0+uPmI9AOTEfoZ1EkdftV6u6pdbLw2/oLT8B9K0kqbiJ81tTIaYaz+0Vr2Y+MqbBJKsYi3OItk6tNC0kZBGKb/AKq9fdCdGLeuRqrUMWA9sK24KFebKdH8DKcrI++MD1Iqunp74t7T1L1hadGta9vXTbTdwlqhsORULQ6hsj9V5rgeDLOSANzLaAFKG5JGVVLa/wDSro74VtNyNYXG1fpLqNa/+ml3xxMqZLk4ynaVDakjBJcCQQASTxW/q3h+t45fUuq5Pji0fctKQNTXDpK1PZL9rt8uOEXC7tJVw8rKhmPlJBQ0SeASvHwl5fCZ04vvS/pRB03qq126LqC3vOMSblbtpTdEhWUSVKACitSSAorG4qSonuDVOnUnxTar1D18i9R4VyP4papyZUNxJUGyUkAoCc5DRSNgT+7nPKlE2X9Ovaj9FtVWyIq+XKfpK4qQnzmZ8Fx1tK8fEEraC8pz2Jxx6Csn9ZLvuJlgYpa4bpt1u0L1eZdd0dqq16h8oBTrcKQlbjQPYrR8yfzAruat0FFFFBoX81FC/mooNx4rWJTRe8rzE+bjdsyM4+ua4rq5r9zQmnGzAZE2/wByeTAtcMnAckLzhSvohABWo+iUmmi6H6bmXHVFvufvDlw93eemvXp9OH7ghxtbYccV6JcWrc00OENMoJ5WmptTbiS2eM1iXEg4zUX/ABw+MJzwu6UtYsDFsvOrrk+PKts5xXwRglRcfKUqCiMpCRyOVeuCKbTw8+0xj9V9MXtm76SX+m0IpXGtNoeSG5rasJCkqeUNpDhSkpypR3pKQfiww2Ju37UVs0vZ5d1u8+PbLbEbLr8uW6G2mkDuVKJwBVX3i69qJNv5naV6PvOwLf8AE1I1OtBS+6Ox93SeWx/GRu54Ce5bbVepOtXtBdTXV64rTo7prp9Tj09T6lN221obBK1OHu++Eg8en8ANQ3uDjQkPtQ1LMJLig2pwBK3EhR2qWB64xwOBU26m+WtU2Y/cJD0mS+5JkPLLjjzqipbiickqJ5JJOcmrB/DZ4abJ1d0LYtN35+5uRGJ8VTltjS/JZK/LLzrriAPiGxDyAe4U6jGMk1ACxtJfvUBtTSn0rkNpLSMbljcOB/OrMPCv1m0x0nu+or5e3Vu+faUfhkWOMrkOBweY2hP76tzXJwEhCicAGsQ9jxg+DToTpC02t6FaZOkp0p591H4K4ta5SsIAZCFhaEpyrcPlA2q+JIJIhx4jOsd7kWm2aUl3+XeZUSGmH5sl7zFRIo+VkKCRuUoBO5ZG5WBnAwA4fiZ8VNw1TdZN1uMtl7UCkliDa453M25knO3PBJ9So8qOOAkACGMuY7NkvSZDqnn3VFbji+VKJ7mjfrWB2rJWArjOPTNago7yPSs93PNA8nhF62udAuvml9UrdW3ai+IV0SnsqI6Qlwkeu3IWPugV+gWNIbksNutLS424kKStJyFA8givzLZq9n2ffVVzqv4XdIS5LxduNpbNllqJyStjCUE/ct+Wo/c1XirxSVopB2FLVujQv5qKF/NRQRi6takuGquusjTNugImvQ7amC2t94tIjl8oXJUFBKjuWwQgEAFIJPOcVzvic8TM3wteHLTmpLHb4EvUmq5SPLalbvKbDjJcUoAYKg2gNtpBxwE/TFOD1i6WxYmupms4ynLfc5Udks3ASC0yl9rgtvLwfLS62EJDnABRyeUgs91eTZLnpuHC1Uxe9RWOAlx636TfsiC40kNrCkIlp3BxtDatu9pDjoSMpIJJrk48vtVHfL7N1xIeu10nyLpIluFEp+4vF15l5RJSvecHYon+Q+LjO0n6NN63vfTLUbF70k47Zbq3E91TcIhJI3tbXSM52rIKgcHjnABrx9YzbFI1Pcn9LwH4FlfUryYslwrKElWQkc5CRxgKUo8cnnA8MuuKJKyc4Ce/cDmsYtB6Sa4k9ffZl9QbFEi/h9705CkR5LkdIbTMDW2UV8Y+JaMpV9VZPY4qr7nj0B/vUk7hqHXvQPwzW7SU6U7C071Nhybkm2BkR5UVxqQ2hLql4ClNPNNpGxRwUqJx9Y5yUENRlbSkKayn74UUk/1Sa1rGFLcgS2JTKsOsuJcSfoUnI/4p6dX9XYsO3OLt2HrnOG/IJSI7ZAxkjGSSCcevGcgAUyAH9aMcY7GsMK+6p5xTiyVLWdxJ9TWG3IJJxj0pcgnGaX5j/mtCD+9IORwfzrJIA7UK2jj69qDEEgDPerVvY2P3RegeobTp/wBFRdI6owx2fLR87/xDNVVbCTVyHslrvYJXhrft1rCkXeHeZCrslfdTqwktrH8JaS2n+aFVs62dTfHYUtIOBS10dWhfzUUL+aig2rQlxJSoZB4IPrXk2/SNks8iRIgWeBCfkDDzsaMhtbn+4gAn869iiswVoeLj2f3TO2akiSdKKvNnvd+fkTHIERaHYcdhtBW6tLZTuA3qbG0K4SpRAIRinC6EeC3o50xhfit00Zdb/quyOpS47fH23Ul1I3ealpLnkITxkFwkJ7biRmpedStEOat0/NVbJAtuo2ojzdvuO0K8pak8JWkghxoqCdyFAg47ZAIpR8RfiB62GTO0NrCK5oCMUJRKsNsjLhsyQM5USVKK21HcralXl5USByaizHKzI+Hxv+IJzxCdcJtxjlkWG0N/hdsTGXvQW0kla92Bu3LKjkcY24z3LFPuedaoec72FLayewSSFJH9SuvjAwK+yPb5si2TJbUdxyBGW2mQ8B8Da1bg2CfqcLwPXB+lYx8fc9v6UiRjJ9ayPbt/WgnGR/egwV9O350gJx3z9s0qucAkj6UYIGP7UGKCVEg8Y5oJBI9Mds1kAUjvSHJOMd/WgMndyc1cF7Ie52mT4ebzDiR22brEvz3vy0/M7uaaLa1fbblI/wBh+pqn3aB2qzb2My5qEdUUKYd/DSq3lD5SfLLo8/ckHtnaUkj7j61s62dWdUtIO1LXR1aF/NRQv5qKDfRRRQIeRTddaugWievulXLDrKzM3GPyWJAG2RFWR87TndB/sfUEc041FBUjrj2PnUBjWEpnR+qLFM0ypW6PJvLrrMpCT+ytLbSkkj94EA/Qdq2eNXw/2XwneETRuiLe6iferzqFE67XbZtVLcajujAHcNp80BKc8cnuo1bVVaPtnrilNs6WQO61vXB/8kpYT/7VzsxFir/Pf0rHisgPT+tYKwPuaxAUonHFIpRA44pScEc85oICgOQB9KMLuJAITk0rDS3nktoQpxxxQQlCRkqJOAAPUmsA38YwcYqbnsl7XZbr4kLmi52+NNmR7G7KgOyGgsx3UvMgqRn5VbVEZHOM/WjW/wAMfsvda9VFQr71BL2idMLKXBCWj/UpSO/CCMMg/Vfxfw+tWwdNOlOl+kOkoemtJWliy2iKPhZYTytXqtajytRxyokkV1wGBxS1cjpJhBwaWiiqU0L+aihfz0UG+iiigKKKKAqq/wBsy8pWsOl7RPwJgz1AfcuM5/4NFFT5cTeK4/8A7WtaQSftRRUObXuPmp+9ZFP6z8qKKMjIfODUxPZTvLa8WcNKTw5ZpqFfcfAf+QKKKKXVjtS0UV1dRRRRQaF/NRRRQf/Z';
    result = {'code': '408'}
    if 'window.code=408' in rep.text:
        # 用户没有扫码
        result['code'] = 408
    elif 'window.code=201' in rep.text:
        # 用户扫码，没有确认登录
        result['avatar'] = re.findall("window.userAvatar = '(.*)';", rep.text)[0]
        result['code'] = 201
    # print(rep.text)  # 如果返回window.code=200则确认登录
    # window.redirect_uri = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=Ay-w09wa6tpYoi8_49VcmwBn@qrticket_0&uuid=AcpaAnB8rg==&lang=zh_CN&scan=1568596803";
    elif 'window.code=200' in rep.text:
        # 用户确认登录
        redirect_uri = re.findall('window.redirect_uri="(.*)";', rep.text)[0]
        print(redirect_uri)
        # https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A22WujWQbYmgsT5rFV5_mDJd@qrticket_0&uuid=Ieoz30KGUQ==&lang=zh_CN&scan=1568602836
        redirect_uri = redirect_uri + '&fun=new&version=v2'
        ru = requests.get(
            url=redirect_uri,
        )
        print(ru.text)  # 凭证内容
        result['code'] = 200
        ticket_dict = xml_parse(ru.text)
        session['ticket_dict'] = ticket_dict
    return jsonify(result)


@app.route('/index')
def index():
    pass_ticket = session['ticket_dict']['pass_ticket']
    init_url = 'xxx&pass_ticket={0}'.format(pass_ticket)
    rep = requests.post(
        url=init_url,
        json={
            'BaseRequest': {
                'DeviceID': 'xxx',
                'Sid': session['ticket_dict']['wxsid'],
                'Skey': session['ticket_dict']['skey'],
                'Uin': session['ticket_dict']['wxuin'],
            }
        }
    )
    rep.encoding = 'utf-8'  # 内部拿到字节转换成字符串
    # json.loads将字符串转换成json，但是内部会做，使用rep.json
    init_user_dict = rep.json()
    print(init_user_dict)
    return render_template('index.html', init_user_dict=init_user_dict)


if __name__ == '__main__':
    app.run()
