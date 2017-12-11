import binascii
import json
import re
import urllib

from fake_useragent import UserAgent
import requests
import rsa
import base64

from config import *
from download import request


class Login(object):

    def __init__(self):
        self.username = USERNAME
        self.password = PASSWORD

    def prelogin(self):
        try:
            json_pattern = re.compile('\((.*)\)')
            url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1512973708859' % self.get_username()
            response = request.get(url, 3)
            # print(response.status_code)
            json_data = re.search(json_pattern, response.text).group(1)
            return json.loads(json_data)
        except:
            print('error')
            return None

    def get_username(self):
        username_url = urllib.parse.quote(self.username)
        username_base64 = base64.b64encode(bytes(username_url, encoding='utf-8'))
        username = username_base64.decode('utf-8')
        # print(username)
        return username

    def get_password(self, data):
        rsa_e = 65537  # 0x10001
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 安全起见清空明文密码
        passwd = binascii.b2a_hex(pw_encypted)
        # print(passwd)
        return passwd

    def post_data_build(self, data):
        post_data = {
            'entry': 'weibo',
            'gateway': '1',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
            'vsnf': '1',
            'su': self.get_username(),
            'service': 'miniblog',
            'servertime': data['servertime'],
            'nonce': data['nonce'],
            'pwencode': 'rsa2',
            'rsakv': data['rsakv'],
            'sp': self.get_password(self.prelogin()),
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': '78',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }
        return post_data

    def login(self):
        session = requests.Session()
        post_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        data = self.post_data_build(self.prelogin())
        response = session.post(post_url, headers=headers, data=data)
        p = re.compile('location\.replace\(\"(.*?)\"\)')
        response = session.get(p.search(response.text).group(1),)
        p = re.compile('location\.replace\(\'(.*?)\'\)')
        response = session.get(p.search(response.text).group(1))
        p = re.compile(r'"userdomain":"(.*?)"')
        url = 'https://weibo.com/' + p.search(response.text).group(1)
        response = session.get(url)
        print(response.text)

        return None


if __name__ == '__main__':
    Login().login()
