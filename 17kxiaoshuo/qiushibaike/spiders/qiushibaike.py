import scrapy

class Xiaoshuo17k(scrapy.Spider):#要使用 scrapy 爬虫，继承  scrapy.Spider 这个类，这样才能使用它定义的一些方法
    name = "qiushibaike"        #定义一个爬虫的名称

#定义我们的请求
    def start_requests(self):
        urls = [
            'https://www.17k.com/book/3006464.html',
            'https://www.17k.com/book/3006465.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  #参数 callback=self.parse 回调数据解析方法

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '17k-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)