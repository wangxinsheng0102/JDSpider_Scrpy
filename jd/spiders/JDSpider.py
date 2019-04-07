import scrapy

from jd.items import JDItem
import urllib.parse

class JdSpider(scrapy.Spider):
    name = "jingdong"
    allow_domins = ['search.jd.com']
    main_class = "生鲜"
    k = input()
    keyword = urllib.parse.quote(k)
    base_url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % keyword
    page = 1
    start_url = [base_url+'&page=' + str(page) +'&click=0']
    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse, meta={'page': self.page}, dont_filter=True)
    def parse(self, response):
        #商品列表
        products = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        #列表迭代
        for product in products:
            item = JDItem()
            try:
                img_url = ''.join(product.xpath('.//div[@class="p-img"]/a/img/@src').extract()[0])
            except:
                img_url = ''
            try:
                name =  ''.join(product.xpath('.//div[@class="p-name"]/a/em/text()').extract()).strip().replace(' ','')
            except:
                name = ''
            if name == '':
                try:
                    name = ''.join(product.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()').extract()).strip().replace(' ','')
                except:
                    name = ''
            try:
                price = product.xpath('.//div[@class="p-price"]//i/text()').extract()[0]
            except:
                price = ''

            try:
                store = product.xpath('.//div[@class="p-shopnum"]//a/@title').extract()[0]
            except:
                store = ''
            try:
                evaluate_num = product.xpath('.//div[@class="p-commit"]/strong/a/text()').extract()[0]
            except:
                evaluate_num = ''
            try:
                detail_url = product.xpath('.//div[@class="p-name p-name-type-2"]/a/@href').extract()[0]
            except:
                detail_url = ''
            try:
                if product.xpath('.//div[@class="p-icons"]/i/text()').extract()[0] == '自营':
                    support = '自营'
                else:
                    support = '非自营'
            except:
                support = '非自营'
            item['name'] = name
            item['price'] = price
            item['store'] = store
            item['evaluate_num'] = evaluate_num
            item['detail_url'] = detail_url
            item['support'] = support
            item['first_class'] = self.main_class
            item['second_class'] = urllib.parse.unquote(self.keyword)
            item['img_url'] = img_url
            # 这里的yield将数据交给pipelines
            yield item
            print(item)
            # 这里的目的是配合middlewares中的slenium配合，这里每次都要打开相同的网页self.base_url,然后运用selenium操作浏览器，在最下方的页码中输入要查询的页数，我们这里查询1-100页
        if self.page < 10:
            self.page += 1
            print(self.page)
            # 这里的meta使用来传递page参数，dont_filter表示不去重，因为scrapy默认会去重url，我们每次请求的网页都是重复的，所以这里不去重
            yield scrapy.Request(url=self.base_url, callback=self.parse, meta={'page': self.page}, dont_filter=True)