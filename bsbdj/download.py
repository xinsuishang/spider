import random
import re
import time

import requests
from fake_useragent import UserAgent


class download():

    def __init__(self):

        self.iplist = []
        self.ua = UserAgent()
        header = {'User-Agent': self.ua.random}
        for page in range(1, 11):
            ip_url = 'http://www.xicidaili.com/nn/' + str(page)
            response = requests.get(ip_url, headers=header)
            self.iplist += re.findall(r'\d+\.\d+\.\d+\.\d+', response.text, re.S)

        # self.user_agent_list = [
            # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            # "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            # "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            # "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            # "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            # "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        # ]

    def get(self, url, timeout, proxy=None, num_retries=6):
        # UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': self.ua.random}
        headers['referer'] = url

        if proxy is None:  # 当代理为空时，不使用代理获取response
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_retries > 0:  # num_retries 限定重试次数
                    time.sleep(10)  # 延迟十秒
                    print('downs', '获取网页出错，10S后将获取倒数第： %s次' % num_retries)
                    print('downs', url)
                    return self.get(url, timeout, num_retries=num_retries - 1)  # 调用自身,并将次数减1
                else:
                    print('downs', '开始使用代理')
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy,)

        else:
            try:
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)  # 使用代理获取response
            except:

                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print('downs', '正在更换代理，10S后将重新获取倒数第 %s次' % num_retries)
                    print('downs', '当前代理是：%s' % proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print('downs', '代理也不好使了！取消代理')
                    return self.get(url, 3)


request = download()
