# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestproItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()  # 公司名称
    job_name = scrapy.Field()  # 职位名称
    salary = scrapy.Field()  # 薪资
    address = scrapy.Field()  # 地址
    company_url = scrapy.Field()  # 公司主页网址

    pass
