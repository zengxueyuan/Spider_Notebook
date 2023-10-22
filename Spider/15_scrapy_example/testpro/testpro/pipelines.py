# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv


class TestproPipeline:
    # 爬虫启动时执行一次的方法
    def __init__(self):
        self.f_csv = None
        self.headers = None

    def open_spider(self, spider):
        self.headers = ["company", "job_name", "salary", "address", "company_url"]
        # 打开csv文件添加表头
        with open("../../tmp/C_data.csv", "a+") as f:
            self.f_csv = csv.writer(f)
            self.f_csv.writerow(self.headers)

    # 默认处理数据的方法
    def process_item(self, item, spider):
        # 从Item中取出数据，写入csv文件
        rows = [item["company"], item["job_name"], item["salary"], item["address"], item["company_url"]]
        with open("../../tmp/C_data.csv", "a+") as f:
            self.f_csv = csv.writer(f)
            self.f_csv.writerow(rows)

        return item
