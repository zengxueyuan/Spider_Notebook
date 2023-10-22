# import scrapy
# from bs4 import BeautifulSoup
# import json
# from testpro.items import TestproItem
# from selenium import webdriver
# import time
#
#
# class WyjobSpider(scrapy.Spider):
#     # 定义爬虫名
#     name = "51job"
#     allowed_domains = ["we.51job.com"]
#     start_urls = ["http://we.51job.com/"]
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
#         "Cookie": "guid=217439c78f1cfa2e843094c3ce8d83fd; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; Hm_lvt_1370a11171bd6f2d9b1fe98951541941=1696404683,1697075932; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22217439c78f1cfa2e843094c3ce8d83fd%22%2C%22first_id%22%3A%2218af9993328153a-05d3aecf78074e-78505775-1296000-18af9993329165f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThhZjk5OTMzMjgxNTNhLTA1ZDNhZWNmNzgwNzRlLTc4NTA1Nzc1LTEyOTYwMDAtMThhZjk5OTMzMjkxNjVmIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjE3NDM5Yzc4ZjFjZmEyZTg0MzA5NGMzY2U4ZDgzZmQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22217439c78f1cfa2e843094c3ce8d83fd%22%7D%2C%22%24device_id%22%3A%2218af9993328153a-05d3aecf78074e-78505775-1296000-18af9993329165f%22%7D; acw_tc=ac11000116977042646931073e00df5a7741093e14f909dba9264ff43d0961; acw_sc__v2=6530e94a8e9ceeb26531ce85b2747695bfd2a79c; JSESSIONID=0A2508A7F0D7C1F737D70932B88F0C66; ssxmod_itna=euGQBKD5Yvoh8DzxAOe5DkFvqDIob20TbeynPDswrDpxBFeidTo1rP1PN1o5ElDQupoTSm8rvwq4UAi3tob1lFhYDU4i8X48=TeDxx0oD5xGoDPxDeDADKiTDY4Ddfh5H=DEDeKDR8x0kXAI41lI8mxGCMxDCDGFFDQKDucF5DGvb3=4D4xGrDm+82pa+6eoDnPWCeAKD9=oDsZij1AKwRbk5cPyfeD83mxYGDCKDjc+8Dmndr4Gd615ABQr3PGbapl03xg04KPeKAW047G2D3GGPamiioBZHFCwlDDcD17haxoD; ssxmod_itna2=euGQBKD5Yvoh8DzxAOe5DkFvqDIob20TbeyeikANdN5Dl=npDj+K=0QT3oTX1nmrq9GGPTldBwG1zxAp+q0pMOnE0GKC+2vP4tcvu6wjcaM0vT=ej0TQv2ZClFjurMlZSSjdwyBZ234LEFBUpfrKgAE00lfKmekr8Gnr8z0jyACA/l+UnjORfRhTdrqY5Pa0m34waq=dF1Pqst6j8rfF7f6c8HYEEnjTry4yrk=LLeP7rr=dXtUYX03SM34AEqRi8CSGCSA=GGfOXGf0dqNwiq5hfyKv7HvBmC4vLvXG8n1M4mXYv3DYH+CDe=Tx3zRGL2HoQFXx3DEaKlrX7dtgiX7oCubX0GXxKanTmko00GfEoGmK/0shCsA2soMphRsfRsNdKUTI6mHkTaAuWBmYnDYPddMQdecdBTWnTduTaOhE7rm6dfdZ=ikkRqfzCEwePD7Q5jDCjGIYeH7wXPeKiFuFen+xctG=DGcDG7=EquaXPYtw7D4D",
#         # "Referer":
#     }
#
#     # 构造职位请求url，获取职位列表
#     def start_requests(self):
#         for pg in range(1, 2):
#             # 构造请求
#             url = "https://we.51job.com/api/job/search-pc?api_key=51job&timestamp=1697078872&keyword=python&searchType=2&function=&industry=&jobArea=000000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum={pg}".format(
#                 pg=pg)
#
#             # yield的作用就是将右边的请求交付给引擎
#             yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
#
#     # 接受列表页相应，解析出每个职位的职位信息，构建item并返回给引擎
#     def parse(self, response):
#         soup = BeautifulSoup(response.text, "lxml")
#         # 利用有id属性的div标签，获取标签文本
#         # ??? 有问题
#         data_text = soup.find("div", {"id": "app"}).find_next("div", {"class": "job-list"})
#
#         # 将json格式转换成python的字典类型
#         data_dict = json.loads(data_text)
#
#         for job in data_dict:
#             company = job.find("right").getText()
#             company_url = job.find("right")
#             job_name = job.find("title flex align-center")
#
#             # ..... 未完成 ......
#


### 下面是官网给出的代码

import scrapy
import json
from bs4 import BeautifulSoup
from testpro.items import TestproItem


class WyJobSpider(scrapy.Spider):
    # 定义爬虫名
    name = '51job'
    allowed_domains = ['search.51job.com', 'jobs.51job.com']
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    def start_requests(self):
        for pg in range(1,2):
            url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,{pg}.html?' \
                  'lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99' \
                  '&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(pg=pg)
            yield scrapy.Request(url=url, headers = self.header, callback=self.parse)

    # 接收列表页响应，解析出每个职位的职位信息，构建item并返回给引擎
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # 利用有id属性的div标签，定位与之相邻的script标签，获取标签文本
        data_text = soup.find('div', {'id': 'app'}).find_next('script', {'type': 'text/javascript'}).string.split('=',1)[1]
        # 将json格式转换成python的字典类型
        data_dict = json.loads(data_text)
        # 获取职位信息列表
        job_list = data_dict["engine_search_result"]
        # 遍历职位列表，获取每个职位的信息并生成Item，返回给引擎
        for job in job_list:
            company = job['company_name']
            company_url = job['company_href']
            job_name = job['job_name']
            salary = job['providesalary_text']
            address = job['workarea_text']
            print(company)
            print(company_url)
            print(job_name)
            print(salary)
            print(address)
            print('=' * 100)

            item = TestproItem()
            item['company'] = company
            item['company_url'] = company_url
            item['job_name'] = job_name
            item['salary'] = salary
            item['address'] = address
            yield item

