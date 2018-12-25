# -*- coding: utf-8 -*-
import scrapy
from operator import *
from ..items import DetailItem


class FeekrSpiderSpider(scrapy.Spider):
    name = 'feekr_spider'
    # allowed_domains = ['httpbin.org']
    # start_urls = ['http://httpbin.org/ip']
    allowed_domains = ['www.feekr.com']
    start_urls = ['http://www.feekr.com']

    def __init__(self):
        self.homeList = []

    def parse(self, response):
        list = response.xpath("//div[@class='area clearfix']//a")
        for item in list:
            url = item.xpath(".//@href").extract()[0]
            self.homeList.append(url)
        listUrl = self.homeList.pop()
        print("首页所有连接：" + str(self.homeList))
        print("开始解析页面" + listUrl)
        yield scrapy.Request(url=listUrl, callback=self.parseList)

        # yield HomePageItem(url=url, address=address)

    def parseList(self, response):

        # 列表页的详情页地址
        listPageUrlList = response.xpath("//*[@id='shares_list']/ul/li/a[1]/@href").extract()
        if listPageUrlList:
            for url in listPageUrlList:
                # 遍历开始爬取详情页数据
                yield scrapy.Request(url=url, callback=self.parseDetail)

        # 爬取下一个列表页
        #
        nextPage = response.xpath("//div[@class='pagination']//a[@class='next']//@href").extract()
        if len(nextPage):
            url = nextPage[0]
            print(url)
            yield scrapy.Request(url=url, callback=self.parseList)
        else:
            url = self.homeList.pop()
            print(url)
            yield scrapy.Request(url=url, callback=self.parseList)

    def parseDetail(self, response):
        title = response.xpath("//div[@id='intro']//h2//text()").extract()  # 文章名
        print(title)
        imagesMap = dict()
        image_urls = []
        passageList = []
        title = response.xpath("//div[@id='intro']//h2//text()").extract()  # 文章名
        userName = response.xpath("//meta[@name='author']/@content").extract()  # 用户名
        allImageUrl = response.xpath("//div[contains(@class,'photo-content')]")  # 所有图片
        allText = response.xpath("//div[contains(@class,'text-content')]")
        if allImageUrl:
            for parent1 in allImageUrl:
                parent2 = parent1.xpath(".//li[@class='pic-li']")
                if parent2:
                    for item in parent2:
                        imageurl = item.xpath(".//img/@data-original")[0].extract()
                        imageurl = imageurl[0:imageurl.find('!', 0, len(imageurl))]
                        imagetext = item.xpath(".//div[@class='title ']/p/text()")
                        imageName = ''
                        if imagetext:
                            for text in imagetext:
                                if not eq(text.extract().strip(), ""):
                                    imageName = text.extract().strip()  # 获取图片对应的文字说明
                                    pass
                        image_urls.append(imageurl)  # 获取全部图片
                        imagesMap[imageurl.split('/')[-1]] = imageName
        if allText:
            for parent1 in allText:
                parent2 = parent1.xpath(".//div[@class='desc']/p/text()")
                if parent2:
                    for item in parent2:
                        itemtext = item.extract()
                        if not eq(itemtext.strip(), ""):
                            # print(itemtext.strip())
                            passageList.append(itemtext.strip())
        userImg = response.xpath("//i[@class='avatar']/img/@src").extract()[0]  # 用户头像
        userImg = userImg[0:userImg.find('!', 0, len(userImg))]
        image_urls.append(userImg)
        address = response.xpath("//a[@class='a-address']/text()").extract()[0]  # 旅游地址

        # print("=" * 20)
        # print("title == " + title[0].strip())
        # print("作者 == " + userName[0])
        # print("address == " + address[0].strip())
        # print("userImg == " + userImg)
        # print("map = " + str(imagesMap))
        # print("=" * 20)

        item = DetailItem()
        # 需要下载的图片地址，最后需要放开
        item['image_urls'] = image_urls
        item['title'] = title[0].strip()
        item['userName'] = userName[0].strip()
        item['userImg'] = userImg.split('/')[-1]
        item['address'] = address.strip()
        item['passageList'] = passageList
        item['imageMap'] = imagesMap
        yield item
