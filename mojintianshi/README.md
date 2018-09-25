---
title: urllib、pyquery下载笔趣阁小说
date: 2018-09-25 14:28:04
categories: 编程
tags: python
---

## 一、小说章节路径获取

**1、爬取的小说名为摸金天师，小说首页为http://www.biquge.com.tw/18_18128/，通过urllib.request.urlopen获取页面HTTPResposne类型的对象，在通过read()方法获取页面内容**

```python
request = urllib.request.Request(url, headers=headers)
try:
    content = urllib.request.urlopen(request)
    text = str(content.read(), encoding = 'gbk')
    content.close()
    return text
except urllib.error.URLError as e:
    print(e.reason)
    return ''
```

**2、审查章节元素，获取章节路径**

![chapters](https://upload-images.jianshu.io/upload_images/4605151-9019dc0a25798009.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
def get_all_chapter(self):
    html = self.request(self.url)
    doc = pq(html)
    all_chapters = doc('#list a').items()
    for a in all_chapters:
        text = a.text()
        href = self.domain + a.attr('href')
        self.chapter_titles.append(text)
        self.chapter_urls.append(href)
```

**3、审查页面元素，获取每个章节内容**

![content](https://upload-images.jianshu.io/upload_images/4605151-3aaf6232e001bb2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
def get_content(self, url):
    html = self.request(url)
    doc = pq(html)
    content = doc('#content').text()
    content = content.replace('\xa0'*4, '\n\n')
    return content
```

**4、将文章输出txt**

```python
def write (self, name, path, txt):
        write_flag = True
        with open(path, 'a', encoding = 'utf-8') as f:
            f.write(name + '\n')
            f.writelines(txt)
            f.write('\n\n')
```

二、完整代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: sunny

import urllib.request
from pyquery import PyQuery as pq
import sys, random, time

class DownloadNovel():
    def __init__(self, url):
        self.url = url
        self.chapter_urls = []
        self.chapter_titles = []
        self.domain = 'http://www.biquge.com.tw'
        self.sleep_download_time = 5
    def get_all_chapter(self):
        html = self.request(self.url)
        doc = pq(html)
        all_chapters = doc('#list a').items()
        for a in all_chapters:
            text = a.text()
            href = self.domain + a.attr('href')
            self.chapter_titles.append(text)
            self.chapter_urls.append(href)
    def get_content(self, url):
        html = self.request(url)
        doc = pq(html)
        content = doc('#content').text()
        content = content.replace('\xa0'*4, '\n\n')
        return content
    def write(self, name, path, txt):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(txt)
            f.write('\n\n')
    def request(self, url):
        time.sleep(self.sleep_download_time)
        # 动态userAgent
        user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        ua = random.choice(user_agent_list)
        headers = {
            'User-Agent': ua
        }
        request = urllib.request.Request(url, headers=headers)
        try:
            content = urllib.request.urlopen(request)
            text = str(content.read(), encoding = 'gbk')
            content.close()
            return text
        except urllib.error.URLError as e:
            print(e.reason)
            return ''

if __name__ == '__main__':
    dl = DownloadNovel('http://www.biquge.com.tw/18_18128/')
    dl.get_all_chapter()
    for i in range(len(dl.chapter_titles)):
        print('url=%s, title=%s' %(dl.chapter_urls[i],dl.chapter_titles[i]))
        txt = dl.get_content(dl.chapter_urls[i])
        dl.write(dl.chapter_titles[i], '摸金天师.txt', txt)
        sys.stdout.write('  已下载:%.3f%%' % float(i/len(dl.chapter_titles)) + '\r')
        sys.stdout.flush()
    print('下载完成')
```

三、效果

![效果](https://upload-images.jianshu.io/upload_images/4605151-1e2236300bcb3142.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

四、源码

源码[链接](https://github.com/sunnyShining/python-spider/tree/master/mojintianshi)