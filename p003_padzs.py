import requests
from bs4 import BeautifulSoup

def request_geilimei(url):
   try:
       response = requests.get(url)
       if response.status_code == 200:
           return response.text.encode('iso-8859-1').decode('gbk')
   except requests.RequestException:
       return None

def write_item_to_file(soup):
   item_name = soup.head.title.string
   head=soup.find(class_='novel_title').text
   nr= soup.find(class_='novel_content').text
   print('开始写入数据 ====> ' + item_name)
   with open('book_1.txt', 'a', encoding='utf-8') as f:
       f.write(head+ '\n')
       f.write(nr+ '\n')

def main(page):
    url = 'https://www.geilimei.cc/files/article/html/15/15819/'+str(page+1410772)+'.html'  #334504
    html = request_geilimei(url)
    soup = BeautifulSoup(html, 'lxml')
    write_item_to_file(soup)

if __name__ == "__main__":
   for i in range(0,18):
       main(i)