from bs4 import BeautifulSoup
import os
from download import request
from pymongo import MongoClient
from config import *

client = MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


class mzitu():

    def __init__(self):
        self.collection = db[MONGO_TABLE]
        self.title = ''  # 用来保存页面主题
        self.url = ''  # 用来保存页面地址
        self.img_urls = []  # 初始化列表保存图片地址

    def all_url(self, url):
        html = request.get(url, 3)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            self.title = title
            print(u'开始保存：', title)
            path = str(title).replace("?", '_')
            self.mkdir(path)
            href = a['href']
            self.url = href
            if self.collection.find_one({'主题url': href}):  # 判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
                print(u'这个页面已经爬取过了')
            else:
                self.html(href)

    def html(self, href):
        html = request.get(href, 3)
        max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[10].get_text()
        page_count = 0
        self.img_urls = []
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            page_count += 1
            self.img(page_url, max_span, page_count)

    def img(self, page_url, max_span, page_count):
        img_html = request.get(page_url, 3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        self.save(img_url)
        if int(max_span) == page_count:
            post = {'标题': self.title,
                    '主题url': self.url,
                    '图片地址': self.img_urls}
            self.save_to_mongo(post)

    def save(self, img_url):
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): 
        abspath = os.path.join('/Users/admin/Desktop/spider/spider/mzitu/img_test', path)
        path = path.strip()
        is_exists = os.path.exists(abspath)
        if not is_exists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(abspath)
            os.chdir(abspath)
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            os.chdir(abspath)
            return False

    def save_to_mongo(self, result):
        if db[MONGO_TABLE].insert(result):
            print('Successfully Saved to Mongo', result['标题'])
            return True
        return False


Mzitu = mzitu()  # 实例化
Mzitu.all_url('http://www.mzitu.com/all')  # 入口
