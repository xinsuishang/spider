import multiprocessing
import os
import threading
import time

from bs4 import BeautifulSoup

from config import ROOT
from download import request
from log import Log
from MongoQueue import MogoQueue

crawl_queue = MogoQueue('mzitu', 'crawl_queue')  # 所有的主题url
SLEEP_TIME = 1


def mzitu_crawler(max_threads=10):
    img_queue = MogoQueue('mzitu', 'img_queue')  # 这个是图片实际URL的队列

    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                Log.info('spider', url)
            except KeyError:
                Log.info('spider', '队列没有数据')
                break
            else:
                img_urls = []
                html = request.get(url, 3).text
                title = crawl_queue.pop_title(url)
                path = str(title).replace("?", '_')
                mkdir(path)
                try:
                    max_span = BeautifulSoup(html, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                    for page in range(1, int(max_span) + 1):
                        page_url = url + '/' + str(page)
                        img_html = request.get(page_url, 3)
                    try:
                        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
                        img_urls.append(img_url)
                        save(img_url)
                    except AttributeError:
                        pass
                    crawl_queue.complete(url)  # 设置为完成状态
                    img_queue.push_imgurl(title, url, img_urls)
                    Log.info('spider', '插入数据库成功')
                except AttributeError:
                    pass

    def save(img_url):
        name = img_url[-9:-4]
        Log.info('spider', u'开始保存：%s' % img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(path):
        abspath = os.path.join(ROOT, 'img_test', path)
        path = path.strip()
        is_exists = os.path.exists(abspath)
        if not is_exists:
            Log.info('spider', u'建了一个名字叫做%s的文件夹！' % path)
            os.makedirs(abspath)
            os.chdir(abspath)
            return True
        else:
            Log.info('spider', u'名字叫做%s的文件夹已经存在了！' % path)
            os.chdir(abspath)
            return False

    threads = []
    while threads or crawl_queue:
        """
        这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
        """
        for thread in threads:
            if not thread.is_alive():  # is_alive是判断是否为空,不是空则在队列中删掉
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():  # 线程池中的线程少于max_threads 或者 crawl_qeue时
            thread = threading.Thread(target=pageurl_crawler)  # 创建线程
            thread.setDaemon(True)  # 设置守护线程
            thread.start()  # 启动线程
            threads.append(thread)  # 添加进线程队列
        time.sleep(SLEEP_TIME)


def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    Log.info('spider', '启动进程数: %d' % num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler)  # 创建进程
        p.start()  # 启动进程
        process.append(p)  # 添加进进程队列
    for p in process:
        p.join()  # 等待进程队列里面的进程结束


def all_url(url):
    html = request.get(url, 3)
    all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        href = a['href']
        # Log.info('spider', '插入成功 title=%s href=%s' % (title, href))
        crawl_queue.push(href, title)


if __name__ == '__main__':
    """
    首先释放all_url，获取到要爬取的所有主题链接
    然后使用process_crawler()，开始爬取图片
    """
    # all_url('http://www.mzitu.com/all')  # 入口
    process_crawler()
