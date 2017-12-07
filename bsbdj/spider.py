import re

import download


def start(url):
    response = download.request.get(url, 3)
    pattern = re.compile('<div.*?j-list-user">.*?class="u-user-name".*?>(.*?)<.*?fr">(.*?)<.*?list-c">.*?href.*?">(.*?)<', re.S)
    items = re.findall(pattern, response.text)
    for item in items:
        print('%s %s \n%s' % (item[0], item[1], item[2].strip()))


if __name__ == '__main__':
    for page in range(1,51):  #  百思不得姐的text页面只显示到50页
        url = 'http://www.budejie.com/text/' + str(page)
        start(url)
    
