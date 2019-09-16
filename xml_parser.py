# coding:utf-8
from bs4 import BeautifulSoup


def xml_parse(text):
    '''
    xml转换为字典
    :param text:
    :return:
    '''
    result = {}
    soup = BeautifulSoup(text, 'html.parser')
    tag_list = soup.find(name='error').find_all()
    # print(tag_list)  # 列表
    for tag in tag_list:
        # print(tag.name, tag.text)  # ret 1203
        result[tag.name] = tag.text
    # print(result)
    return result


text = '<error><ret>1203</ret><message>为了你的帐号安全，此微信号已不允许登录网页微信。你可以使用Windows微信或Mac微信在电脑端登录。Windows微信下载地址：https://pc.weixin.qq.com  Mac微信下载地址：https://mac.weixin.qq.com</message></error>'
ret = xml_parse(text)
