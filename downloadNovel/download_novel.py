#！/usr/bin/env Python3
# -*- coding:UTF-8 -*-

import urllib.request
import string, ssl, sys
from bs4 import BeautifulSoup

class DownloadNovel():
    def __init__ (self, server):
        self.server = server
        # 存放章节名
        self.chapterNames = []
        # 存放章节链接
        self.chapterUrls = []
        # 存放章节数
        self.nums = 0
    def get_download_chapter_url (self):
        # 用于爬取https
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(self.server, context = context)
        text = str(response.read(), encoding = 'utf-8')
        bf = BeautifulSoup(text, 'html.parser')
        div = bf.find_all('div', class_ = 'volume')
        for i in range(len(div)):
            li = div[i].find_all('li')
            for j in range(len(li)):
                a = li[j].find_all('a')
                html = BeautifulSoup(str(a), 'lxml')
                # 章节url
                self.chapterUrls.append('https:' + str(html.a.get('href')))
                # 章节名
                self.chapterNames.append(html.a.string)
    def get_contents (self, target):
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(target, context = context)
        text = str(response.read(), encoding = 'utf-8')
        bf = BeautifulSoup(text, 'html.parser')
        txts = bf.find_all('div', class_='read-content j_readContent')
        txts = txts[0].text.replace('\xa0'*8, '\n\n')
        return txts
    def write (self, name, path, txt):
        write_flag = True
        with open(path, 'a', encoding = 'utf-8') as f:
            f.write(name + '\n')
            f.writelines(txt)
            f.write('\n\n')

if __name__ == '__main__':
    dl = DownloadNovel('https://book.qidian.com/info/1012053141#Catalog')
    dl.get_download_chapter_url()
    print('开始下载')
    for i in range(len(dl.chapterNames)):
        dl.write(dl.chapterNames[i], '无限火力大暴走.txt', dl.get_contents(dl.chapterUrls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/len(dl.chapterNames)) + '\r')
        sys.stdout.flush()
    print('下载完成')