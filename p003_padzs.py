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
   with open('%s.txt'%bookname, 'a', encoding='utf-8') as f:
       f.write(head+ '\n')
       f.write(nr+ '\n')

def main():
    base='https://www.geilimei.cc/files/article/html/3/3333/'
    baseurl=base+'index.html'
    html2 = request_geilimei(baseurl)
    soup2 = BeautifulSoup(html2,'lxml')
    global bookname
    bookname = soup2.find(class_='wp').find(class_='novel_nav').find('h2').find_all('a')[2].text
    list = soup2.find(class_='novel_volume').find_all(class_='novel_list')
    urls3=[]
    for item in list:
        url3=item.find_all('a')
        urls3=urls3+url3
    for url3 in urls3:
        url2=url3.get('href')
        url = base+url2
        html = request_geilimei(url)
        soup = BeautifulSoup(html, 'lxml')
        write_item_to_file(soup)

if __name__ == "__main__":
       main()