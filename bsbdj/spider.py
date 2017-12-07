import re

import download


class Bsbdj(object):
    def __init__(self):
        self.pageIndex = 1
        self.stories = []
        self.go = True

    def getPage(self, pageIndex):
        url = 'http://www.budejie.com/text/' + str(pageIndex)
        response = download.request.get(url, 3)
        if response.status_code == 200:
            return response.text
        else:
            print('请求第 %d 页错误' % pageIndex)
            return None
    
    def getItems(self, pageIndex):
        page_code = self.getPage(pageIndex)
        if page_code:
            pattern = re.compile('<div.*?j-list-user">.*?class="u-user-name".*?>(.*?)<.*?fr">(.*?)<.*?list-c">.*?href.*?">(.*?)<', re.S)
            items = re.findall(pattern, page_code)
            return items
        return None

    def loadStories(self):
        if self.getItems(self.pageIndex):
            self.stories.append(self.getItems(self.pageIndex))
            self.pageIndex += 1

    def getOne(self, page_now):
        self.loadStories()
        try:
            stories = self.stories[0]  # 预加载，全部加载完了
        except IndexError:
            print('全看完了，没有更多的段子了，再见')
            self.go = False
            return 
        del self.stories[0]  # 防止内存爆掉 用完销毁
        if stories is None:
            self.go = False
            return
        for story in stories:
            print('第%d页: %s %s \n%s' % (page_now, story[0], story[1], story[2].strip()))
            get_input = input('Enter键继续，Q退出\n')
            if get_input == 'Q':
                self.go = False
                return

    def start(self):
        self.loadStories()
        page_now = 1
        while self.go:
            self.getOne(page_now)
            page_now += 1


if __name__ == '__main__':
    Bsbdj().start()
