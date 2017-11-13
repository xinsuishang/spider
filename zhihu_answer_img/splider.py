import os
import re

from bs4 import BeautifulSoup
import pandas
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
    }


def save(img_url):  # 保存图片
    name = img_url[-19:-7]
    img = requests.get(img_url, headers=headers)
    f = open(name + '.jpg', 'ab')
    f.write(img.content)
    f.close()


# url = 'http://www.mzitu.com/all/'
url = 'https://www.zhihu.com/people/gou-dan-er-15-93/answers'
start_html = requests.get(url, headers=headers)
img_list = re.findall('img src=\\\&quot;https://(.*?)_hd.jpg', start_html.text)
path = os.path.join('img_test', '狗蛋儿')
if os.path.exists(path):
    pass
else:
    os.mkdir(path)
os.chdir(path)
for i in range(len(img_list)):
    img_list[i] = 'https://' + img_list[i] + '_r.jpg'
    save(img_list[i])
# csv_path = os.path.join(path, 'img_url.csv')
df = pandas.DataFrame.from_dict(img_list).to_csv('img_url.csv')
# soup = BeautifulSoup(start_html.text, 'lxml')
# img_list = soup.find_all('img')
