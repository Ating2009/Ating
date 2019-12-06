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

book=xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet=book.add_sheet('蔡徐坤篮球',cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'地址')
sheet.write(0,2,'描述')
sheet.write(0,3,'观看次数')
sheet.write(0,4,'弹幕数')
sheet.write(0,5,'发布时间')

n=1
def save_to_excel(soup):
    list = soup.find(class_='body-contain').find_all(class_='info')
    for item in list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text
        print('爬取：' + item_title)
        global n
        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)
        n = n + 1

def get_source():
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    save_to_excel(soup)

def search():
    try:
        print('开始访问b站....')
        browser.get("https://www.bilibili.com/")    #访问b站

        # 被那个破登录遮住了，点击一下首页刷新一下
        index = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#primary_menu > ul > li.home > a")))
        index.click()

        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#banner_link > div > div > form > input")))    #获取到b站首页的输入框
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="banner_link"]/div/div/form/button')))           #获取到b站首页的搜索按钮

        input.send_keys('蔡徐坤 篮球')     #输入搜索内容
        submit.click()                    #点击搜索
        print('跳转到新窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])    #切换到新窗口
        WAIT.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="all-list"]/div[1]/div[3]/div/ul/li[1]/button'),str(1)))   #对应页码1
        get_source()
        total = WAIT.until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "all-list"] / div[1] / div[3] / div / ul / li[8] / button')))   #50那个按钮
        return int(total.text)
    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        print('获取下一页数据')
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))  #下一页那个按钮
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),str(page_num)))   #对应页码
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
    book.save(u'蔡徐坤篮球.xls')