from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') #上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
browser = webdriver.Chrome(options=options)
#browser = webdriver.Chrome(options=options, executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe"),executable_path指定Chrome驱动
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400,900)

book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建一个 excel 的 sheet，encoding，设置字符编码，style_compression表示是否压缩
sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  #参数cell_overwrite_ok，表示是否可以覆盖单元格
sheet.write(0, 0, '名称')                                    #每一列就是我们要的关键内容
sheet.write(0, 1, '图片')
sheet.write(0, 2, '排名')
sheet.write(0, 3, '评分')
sheet.write(0, 4, '作者')
sheet.write(0, 5, '简介')

n=1
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
        else :
            item_intr = ''
        print('爬取电影：' + item_index + ' | ' + item_name  +' | ' + item_score  +' | ' + item_intr )
        global n
        sheet.write(n, 0, item_name)                        # 将爬取到的所有数据写入 excel
        sheet.write(n, 1, item_img)
        sheet.write(n, 2, item_index)
        sheet.write(n, 3, item_score)
        sheet.write(n, 4, item_author)
        sheet.write(n, 5, item_intr)
        n=n+1

def get_source():
    try:
        html = browser.page_source
        soup = BeautifulSoup(html,'lxml')
        save_to_excel(soup)
    except TimeoutException:
        browser.refresh()
        return get_source()

def search():
    try:
        print('开始访问豆瓣电影....')
        browser.get("https://www.douban.com")    #访问
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="anony-nav"]/div[1]/ul/li[2]/a')))
        submit.click()
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])    #切换到新窗口
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "db-nav-movie"] / div[2] / div / ul / li[4] / a')))
        submit.click()
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="douban-top250"]/div[1]/h2/span/a')))           #获取到top250按钮
        submit.click()
        WAIT.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/span[2]'),str(1)))  # 这个节点值为页码数1
        get_source()
        total = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/a[9]')))   #10那个按钮
        return int(total.text)
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        print('获取下一页数据')
        next_btn = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/span[3]/a')))  #下一页那个按钮
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/span[2]'),str(page_num)))   #这个节点值为当前页码数
        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)

def main():
    try:
        total = search()
        print(total)
        for i in range(2,int(total+1)):
            next_page(i)
    finally:
        browser.quit()

if __name__ == '__main__':
    main()
    book.save(u'豆瓣最受欢迎的250部电影.xls')




