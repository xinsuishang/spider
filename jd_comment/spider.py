import json
import os

from config import *
from download import request

comment_url = ADDRESS
path = os.path.join(ROOT, FILE_NAME)
if int(SCORE) > 5 or SCORE == 4:
    SCORE = '0'  # 期望获取评论类型为图片或不存在时，重制为获取所有

if SORTTYPE != '5' or SORTTYPE != '6':
    SORTTYPE = '5'  # 排序类型不存在时，重制为推荐排序

if int(PAGESIZE) > 10:
    PAGESIZE = '10'  # 每页最多只能得到10条评论


class JdComment(object):

    def __init__(self):
        self.page = 0  # paga是从0开始的
        self.url = comment_url
        self.next_page = None
        self.params = {
            'productId': PRODUCTID,
            'score': SCORE,
            'sortType': SORTTYPE,
            'page': 50,
            'pageSize': PAGESIZE,
            'isShadowSku': '0',  # 用处未知,不加好像也没有影响
            'fold': '1',  # 用处未知,不加好像也没有影响
        }

    def get_response(self):
        response = request.get(self.url, 3, params=self.params)
        return response.text

    def get_comment(self):
        data = self.next_page
        if data is None:
            return None
        self.next_page = self.get_next_page()
        count = 0
        while True:
            try:
                self.save(data['comments'][count]['content'])
            except IndexError:
                break
            count += 1
        self.get_comment()

    def get_next_page(self, page=0):
        if page == 0:
            self.page += 1
        self.params['page'] = self.page
        data = json.loads(self.get_response())
        if len(data['comments']) == 0:
            return None
        return data

    def mkdir(self):
        if os.path.exists(ROOT):
            return None
        os.mkdir(ROOT)

    def save(self, comment):
        with open(path, 'a') as f:
            comment += '\n'
            f.write(comment)

    def start(self):
        self.next_page = self.get_next_page(-1)
        self.get_comment()


if __name__ == '__main__':
    JdComment().start()
