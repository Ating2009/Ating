import requests
from bs4 import BeautifulSoup
import time
import multiprocessing
import xlwt

book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建一个 excel 的 sheet，encoding，设置字符编码，style_compression表示是否压缩
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  #参数cell_overwrite_ok，表示是否可以覆盖单元格
sheet.write(0, 0, '名称')                                    #每一列就是我们要的关键内容
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

def save_to_excel(soup):
    list = soup.find(class_='grid_view').find_all('li')     # BeatifulSoup 解析
    for item in list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_author = item.find('p').text
        if (item.find(class_='inq')!=None):
            item_intr = item.find(class_='inq').string
        print('爬取电影：' + item_index + ' | ' + item_name  +' | ' + item_score  +' | ' + item_intr )
        item_n=int(item_index)
        sheet.write(item_n, 0, item_name)                        # 将爬取到的所有数据写入 excel
        sheet.write(item_n, 1, item_img)
        sheet.write(item_n, 2, item_index)
        sheet.write(item_n, 3, item_score)
        sheet.write(item_n, 4, item_author)
        sheet.write(item_n, 5, item_intr)
    book.save(u'豆瓣最受欢迎的250部电影.xls')

def request_douban(url):
    try:
        responce=requests.get(url)
        if responce.status_code == 200:
            return responce.text
    except requests.RequestException:
        return None

def main(url):
    html = request_douban(url)
    soup = BeautifulSoup(html, 'lxml')
    save_to_excel(soup)


if __name__ == '__main__':
    start = time.time()
    urls = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(0, 10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        urls.append(url)
    pool.map(main, urls)
    pool.close()
    pool.join()
