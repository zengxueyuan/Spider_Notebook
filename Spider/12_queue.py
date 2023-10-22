# import requests
# import re
# import time
#
# start = time.time()
#
# url = "https://search.damai.cn/searchajax.html"
#
# params = {
#     "cty": "北京",
#     "ctl": "话剧歌剧",
#     "tsg": "0",
#     "order": "1",
#     "pageSize": "30",
#     "currPage": "1",
# }
#
# headers = {
#     "Referer": "https://search.damai.cn/search.htm?",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
#     "Accept": "application/json, text/plain, */*",
#     "X-Xsrf-Token": "f018e78d-380d-4ab9-9202-c3fc24b1056b",
# }
#
# res = requests.get(url, params=params, headers=headers)
# result = res.json()
#
# data = result["pageData"]["resultData"]
# for i in range(len(data)):
#     picture = requests.get(data[i]["verticalPic"])
#
#     # 替换特殊字符
#     invalid_chars = re.compile(r'[\\/:"*?<>|]')
#     name = invalid_chars.sub('_', data[i]["name"])
#
#     with open("./tmp/pics/" + name + ".png", "wb") as file:
#         file.write(picture.content)
#
# end = time.time()
# print("共耗时：", end-start)
import queue

#
# import requests
# import re
# import threading
# import time
#
# start = time.time()
#
# def download_movie(number):
#     for index in range(number*num_per_group, (number+1)*num_per_group):
#         if index < pics_num:
#             picture = requests.get(data[index]["verticalPic"])
#             # 替换特殊字符
#             invalid_chars = re.compile(r'[\\/:"*?<>|]')
#             name = invalid_chars.sub('_', data[i]["name"])
#             # 存入数据
#             with open("./tmp/pics/" + name + ".png", "wb") as file:
#                 file.write(picture.content)
#
#
# url = "https://search.damai.cn/searchajax.html"
#
# params = {
#     "cty": "北京",
#     "ctl": "话剧歌剧",
#     "tsg": "0",
#     "order": "1",
#     "pageSize": "30",
#     "currPage": "1",
# }
#
# headers = {
#     "Referer": "https://search.damai.cn/search.htm?",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
#     "Accept": "application/json, text/plain, */*",
#     "X-Xsrf-Token": "f018e78d-380d-4ab9-9202-c3fc24b1056b",
# }
#
# res = requests.get(url, params=params, headers=headers)
# result = res.json()
#
# data = result["pageData"]["resultData"]
#
# # pictures的数量
# pics_num = len(data)
# # 线程数量
# thread_num = 3
# # 每个线程最多处理多少个图片
# num_per_group = pics_num // thread_num + 1
#
# # 创建线程数组
# threads = []
# for i in range(thread_num):
#     thread = threading.Thread(target=download_movie, args=(i,))
#     thread.start()
#     threads.append(thread)
#
# # 等到所有线程结束
# for thread in threads:
#     thread.join()
#
# end = time.time()
# print("共耗时：", end-start)
#
#
#
# import threading
# import queue
#
# q = queue.Queue()
#
# # 向队列中放入消息
# for item in range(30):
#     q.put(item)
# print("所有消息放入完毕\n", end='')
#
#
# # 使用线程去除队列中的消息
# def worker():
#     while q.qsize() > 0:
#         item = q.get()
#         print(f"处理消息: {item}")
#
#
# # 创建线程
# threads = []
# for i in range(3):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#
# # 启动所有线程
# for t in threads:
#     t.start()
#
# # 等待所有线程完成
# for t in threads:
#     t.join()
#
# print("所有消息处理完毕")


import requests
import re
import threading
import time

start = time.time()


def download_movie():
    while q.qsize() > 0:
        pic = q.get()
        picture = requests.get(pic["verticalPic"])
        # 替换特殊字符
        invalid_chars = re.compile(r'[\\/:"*?<>|]')
        name = invalid_chars.sub('_', pic["name"])
        # 存入数据
        with open("./tmp/pics/" + name + ".png", "wb") as file:
            file.write(picture.content)
        q.task_done()


url = "https://search.damai.cn/searchajax.html"

params = {
    "cty": "北京",
    "ctl": "话剧歌剧",
    "tsg": "0",
    "order": "1",
    "pageSize": "30",
    "currPage": "1",
}

headers = {
    "Referer": "https://search.damai.cn/search.htm?",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
    "Accept": "application/json, text/plain, */*",
    "X-Xsrf-Token": "f018e78d-380d-4ab9-9202-c3fc24b1056b",
}

res = requests.get(url, params=params, headers=headers)
result = res.json()

data = result["pageData"]["resultData"]

# pictures的数量
pics_num = len(data)

# 创建队列
q = queue.Queue()
for pic in data:
    q.put(pic)
print("所有url已放入队列\n")

# 线程数量
thread_num = 3

# 创建线程数组
threads = []
for i in range(thread_num):
    thread = threading.Thread(target=download_movie)
    thread.start()
    threads.append(thread)

# 等到所有线程结束
for thread in threads:
    thread.join()

# 等待所有任务完成
q.join()
print("所有消息处理完毕！")

end = time.time()
print("共耗时：", end - start)
