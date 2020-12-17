import urllib.request
import re
import time
import os
from bs4 import BeautifulSoup


def get_html(url):
    request = urllib.request.Request(url)
    request.add_header(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    )
    response = urllib.request.urlopen(request)
    if response.code != 200:
        print('获取网页失败:', response.code, file='error.text')
        return None
    else:
        print(response.headers)
        html = response.read().decode('utf-8')  # 直接返回会出问题
        print(html)
        return html


def parase_html(html_text):
    soup = BeautifulSoup(html_text, 'lxml')
    # soup.findAll(lambda tag:tag.has_attr('target') and tag.has_attr('href'))
    tag_a = soup.findAll('a',
                         attrs={"target": "_blank"},
                         class_=False,
                         href=re.compile('https://qq.yh31.com/qt/fj/'))
    with open('./images/picture_name.text', 'a+', encoding='utf8') as file:
        for item in tag_a:
            img_type = item.find('img')['src']
            img_name = item.find('img')['alt']
            url = 'https://qq.yh31.com' + img_type
            save_it = img_name + ' https://qq.yh31.com' + img_type + '\n'
            file.writelines(save_it) # item.find('img')['alt'] + url
            if 'jpg' in img_type:
                img_name += '.jpg'
            else:
                img_name += '.gif'
            urllib.request.urlretrieve(url, filename='./images/' + img_name)
def main():
    # List_10.html
    for num in range(1, 11):
        html_text = get_html(
            'https://qq.yh31.com/qt/fj/List_{0}.html'.format(11 - num))
        parase_html(html_text)
        time.sleep(1)


if __name__ == "__main__":
    main()