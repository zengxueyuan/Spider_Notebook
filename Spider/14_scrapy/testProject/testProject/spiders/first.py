import scrapy
from bs4 import BeautifulSoup


class FirstSpider(scrapy.Spider):
    name = "first"
    allowed_domains = ["www.cnur.com"]
    start_urls = ["http://www.cnur.com/rankings/188.html"]

    def parse(self, response):
        # 解析响应，抽取目标数据
        soup = BeautifulSoup(response.text, "lxml")
        # 去掉表头的数据
        tags = soup.find_all("tr", style=";height:30px")[1:]
        # 打印榜单排名信息
        for tag in tags:
            # info1 = tag.strings
            info = list(tag.strings)
            # print(info1)
            # print(info)
            print("2020年度中国高校排名第{}的是{}".format(info[0], info[1]))
            # print("="*80)

        pass
