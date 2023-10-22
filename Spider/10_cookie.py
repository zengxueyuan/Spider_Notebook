# import requests
#
# # 书单页面连接
# url = "https://www.kanman.com/api/getuserinfobook?product_id=1&productname=kmh&platformname=pc&page=1&user_id=260809114&refresh=true&_=1696761852430"
#
# # headers中的Cookie值需要手动在浏览器中登录之后根据实际情况进行替换
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
#     "Referer": "https://www.kanman.com/uc/booklist.html",
#     "Cookie": "koa:sess=ca2a17fe-c162-425f-8894-74b275914c90; koa:sess.sig=HFlx7pq3Cxrq4I0dkpmkvLMHbqo; user=%7B%22Uid%22%3A260809114%2C%22openid%22%3A%2223305584_369D3EDB2C0AD29D5B9EB3328BB678C9%22%2C%22type%22%3A%22mkxq%22%2C%22token%22%3A%221134a4c4e8ce0adeff87170ede79e2d4d6f39b2290085ea26b57da12cfac60be%22%7D; user.sig=N6D7dfpzmTAYi9DYGLcF0O1ELs8",
# }
#
# # 请求结果并转换成JSON格式
# res = requests.get(url, headers=headers)
# json_data = res.json()
#
# # 打印书单中的每部漫画的标题
# for comic_info in json_data["data"]["book_list"][0]["comic_info"]:
#     print(comic_info["comic_name"])



# import requests
# import time
# import random
#
# # 登录操作url
# url = "https://www.kanman.com/login/byuser/"
#
# # 设置登录账号及密码等信息
# data = {
#     "product_id": "1",
#     "productname": "kmh",
#     "platformname": "pc",
#     "identity": "13331093711",
#     "pwd": "Superxiang123",
# }
#
# # 设置请求头，其中最关键的参数是User-Agent
# headers = {
#     "Sec-Ch-Ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#     "Accept": '*/*',
#     "X-Requested-With": 'XMLHttpRequest',
#     "Sec-Ch-Ua-Mobile": '?0',
#     "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
#     "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
# }
#
# res = requests.post(url, headers=headers, data=data)
#
# # 获取cookie信息，以备后续使用
# cookies = res.cookies
# print("请求首页返回的cookie", cookies)
# print("首次连接建立后，服务器会生成cookie信息，跟随响应返回浏览器...此时，我已经拿到cookies信息啦！")
#
# # 让程序随机睡2到5秒，逼真地模仿人类的操作
# time.sleep(random.randint(2, 5))
#
# infobook_page = "https://www.kanman.com/api/getuserinfobook?product_id=1&productname=kmh&platformname=pc&page=1&user_id=260809114&refresh=true&_=1696761852430"
#
# # 发送请求，带上cookie，接受响应
# res = requests.get(infobook_page, headers=headers, cookies=cookies)
# json_data = res.json()
#
# for comic_info in json_data["data"]["book_list"][0]["comic_info"]:
#     print(comic_info["comic_name"])



import requests
import time
import random

# 登录操作url
url = "https://www.kanman.com/login/byuser/"

# 设置登录账号及密码等信息
data = {
    "product_id": "1",
    "productname": "kmh",
    "platformname": "pc",
    "identity": "13331093711",
    "pwd": "Superxiang123",
}

# 设置请求头，其中最关键的参数是User-Agent
headers = {
    "Sec-Ch-Ua": '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "Accept": '*/*',
    "X-Requested-With": 'XMLHttpRequest',
    "Sec-Ch-Ua-Mobile": '?0',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
}

# 创建会话对象
session = requests.Session()

# 发起登录请求
session.post(url, headers=headers, data=data)

print("登录完成，等待2到5秒...")
time.sleep(random.randint(2, 5))

# 使用同个session发起书单页请求
infobook_page = "https://www.kanman.com/api/getuserinfobook?product_id=1&productname=kmh&platformname=pc&page=1&user_id=260809114&refresh=true&_=1696761852430"
res = session.get(infobook_page, headers=headers)
json_data = res.json()

for comic_info in json_data["data"]["book_list"][0]["comic_info"]:
    print(comic_info["comic_name"])

