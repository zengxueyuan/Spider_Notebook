# import time
#
#
# def operate(n, op):
#     with open("./tmp/" + n + ".txt", "a") as file:
#         file.write(op)
#
#
# def cook(n):
#     print("{}洗菜".format(n))
#     operate(n, "洗菜")
#
#     print("{}切菜".format(n))
#     operate(n, "切菜")
#
#     print("{}烧菜".format(n))
#     operate(n, "烧菜")
#
#
# cook("1号厨师")


import threading


def operate(n, op):
    with open("./tmp/" + n + ".txt", "a") as file:
        file.write(op)


def cook(n):
    print("{}洗菜".format(n))
    operate(n, "洗菜")
    print("{}切菜".format(n))
    operate(n, "切菜")
    print("{}烧菜".format(n))
    operate(n, "烧菜")


# t1 = threading.Thread(target=cook, args=("1号厨师",))
# t2 = threading.Thread(target=cook, args=("2号厨师",))
# t3 = threading.Thread(target=cook, args=("3号厨师",))
# t1.start()
# t2.start()
# t3.start()
#
# t1.join()
# t2.join()
# t3.join()
#
# print("开始吃饭！")



# import requests
# import time
#
# start = time.time()
#
# urls = [
#    'https://www.sina.com.cn',
#    'https://www.sohu.com',
#    'https://www.163.com/',
#    'https://www.baidu.com',
#    'https://www.bilibili.com/',
#    'https://www.tmall.com',
#    'https://www.jd.com',
#    'https://www.suning.com',
#    'https://www.tencent.com',
#    'https://www.meituan.com',
#    'https://www.douban.com'
# ]
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
#     "Upgrade-Insecure-Requests": "1",
#     "Cache-Control": "max-age=0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     # "Cookie": "_ntes_origin_from=; _ntes_nuid=ebe2c3c1d574b59820c3057062b47a63; _antanalysis_s_id=1696812219596; W_HPTEXTLINK=old; NTES_PC_IP=%E4%B8%8A%E6%B5%B7%7C%E4%B8%8A%E6%B5%B7",
#
# }
#
#
#
# for url in urls:
#     res = requests.get(url, )
#     print("访问{}结果：{}".format(url, res.status_code))
#
# end = time.time()
# print("共耗时：", end-start)



import requests
import time
import threading

start = time.time()

urls = [
   'https://www.sina.com.cn',
   'https://www.sohu.com',
   'https://www.163.com/',
   'https://www.baidu.com',
   'https://www.bilibili.com/',
   'https://www.tmall.com',
   'https://www.jd.com',
   'https://www.suning.com',
   'https://www.tencent.com',
   'https://www.meituan.com',
   'https://www.douban.com'
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}

# url的数量
urls_num = len(urls)
# 线程数量
thread_num = 3
# 每个线程最多处理多少个网站
num_per_group = urls_num // thread_num + 1


# 爬取一组网址，参数number表示组编号
def crawler(number):
    for index in range(number*num_per_group, (number+1)*num_per_group):
        if index < urls_num:
            res = requests.get(urls[index], headers=headers)
            print("访问{}结果：{}".format(urls[index], res.status_code))


# 创建线程数组
threads = []
for i in range(thread_num):
    thread = threading.Thread(target=crawler, args=(i,))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()

end = time.time()
print("共耗时：", end-start)
