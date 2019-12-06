import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import time

header = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
     'Referer':'http://www.mzitu.com'
     }

def request_page(url):
   #用于下载页面
   r = requests.get(url, headers=header)
   return r.text

def list_page_urls():
    for i in range(9,10):
        baseurl = 'https://www.mzitu.com/page/{}/'.format(i)
        html = request_page(baseurl)
        soup = BeautifulSoup(html, 'lxml')
        list = soup.find(class_='postlist').find_all('li')
        urls=  []
        for item in list:
            url =item.find('a').get('href')
            urls.append(url)
    return urls

def download(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    total = soup.find(class_='pagenavi').find_all('a')[-2].find('span').string
    title = soup.find('h2').string
    image_list = []
    for i in range(int(total)):
        html_tu = request_page(url + '/%s' % (i+1))
        soup_tu = BeautifulSoup(html_tu, 'lxml')
        img_url = soup_tu.select('body > div.main > div.content > div.main-image > p > a > img')[0].get('src')    #find('img').get('src')
        
        image_list.append(img_url)
        time.sleep(0.1)
    path="e:/home/"+title
    os.mkdir(path)                           #建立文件夹
    j = 1
    for item in image_list:                   # 下载图片
        filename = '%s/%s.jpg' % (path,str(j))
        print('downloading....%s : NO.%s' % (title,str(j)))
        with open(filename, 'wb') as f:
            img = requests.get(item,headers =header).content
            f.write(img)
            f.close()
        j+=1


def main():
   # for url in list_page_urls():
   #      download(url)
   #works = len(list_page_urls())
   with ThreadPoolExecutor(max_workers=5) as exector:
       for url in list_page_urls():
           exector.submit(download, url)


if __name__ == '__main__':
   main()