# python3网络爬虫，下载起点小说

## 一、各章小说链接爬取

**1、章节URL：https://book.qidian.com/info/1012053141#Catalog**

**2、经过审查元素各章节名称和链接如下图**

![屏幕快照 2018-07-07 上午9.24.52.png](https://upload-images.jianshu.io/upload_images/4605151-c73ac7110b1867bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**3、可以通过如下方法获取章节名和各章节链接**

```python
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
        print(self.chapterUrls)
        print(self.chapterNames)
```

**4、运行一下效果如下**

![屏幕快照 2018-07-07 上午9.30.27.png](https://upload-images.jianshu.io/upload_images/4605151-954fa89a181c0fb1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 二、爬取所有章节内容，并保存到文件中

**1、爬取章节内容**

![屏幕快照 2018-07-07 上午9.33.11.png](https://upload-images.jianshu.io/upload_images/4605151-4eaffdd9ff3ce388.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看出，小说章节内容全在某个div下，可通过下面方法爬取
```python
    def get_contents (self, target):
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(target, context = context)
        text = str(response.read(), encoding = 'utf-8')
        bf = BeautifulSoup(text, 'html.parser')
        txts = bf.find_all('div', class_='read-content j_readContent')
        txts = txts[0].text.replace('\xa0'*8, '\n\n')
        return txts
```

**2、将文章输出txt**

```python
def write (self, name, path, txt):
        write_flag = True
        with open(path, 'a', encoding = 'utf-8') as f:
            f.write(name + '\n')
            f.writelines(txt)
            f.write('\n\n')
```

## 三、完整代码和效果

**1、完整代码**

```
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
```

**2、效果**

![屏幕快照 2018-07-07 上午9.38.46.png](https://upload-images.jianshu.io/upload_images/4605151-0cec4f9d23b8a56c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![屏幕快照 2018-07-07 上午9.47.04.png](https://upload-images.jianshu.io/upload_images/4605151-22d26d9c5cff0d9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

源码[链接](https://github.com/sunnyShining/python-spider/tree/master/downloadNovel)