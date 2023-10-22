# import requests
#
# # url = "https://comment.kuwo.cn/com.s?type=get_comment&f=web&page=2&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=1b3d5530-5da7-11ee-aa8b-df339d740a53&plat=web_www&from="
# res = requests.get("https://comment.kuwo.cn/com.s?type=get_comment&f=web&page=3&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=f2b904b0-5da6-11ee-aa8b-df339d740a53&plat=web_www&from=")
# res_dict = res.json()
# comments = res_dict["rows"]
#
# for comment in comments:
#     print(comment["msg"])


# import requests
#
# for page in range(1, 4):
#     url = "https://comment.kuwo.cn/com.s?type=get_comment&f=web&page={}&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=1b3d5530-5da7-11ee-aa8b-df339d740a53&plat=web_www&from=".format(
#         page)
#     res = requests.get(url)
#     res_dict = res.json()
#     comments = res_dict["rows"]
#
#     # 循环遍历每条评论并打印出来
#     print("---第{}页评论---".format(page))
#     for comment in comments:
#         print(comment["msg"])


#
# import requests
#
# url = "https://comment.kuwo.cn/com.s"
#
# # 定义请求参数
# params = {
#     "type": "get_comment",
#     "f": "web",
#     "page": "3",
#     "rows": "5",
#     "digest": "2",
#     "sid": "93",
#     "uid": "0",
#     "prod": "newWeb",
#     "httpsStatus": 1,
#     "reqId": "de3bd9d0-5da7-11ee-be91-09b4fcdf5e69",
#     "plat": "web_www",
# }
#
# res = requests.get(url, params=params)
# res_dict = res.json()
# print(res_dict)
# comments = res_dict["rows"]
#
# for comment in comments:
#     print(comment["msg"])


import requests
import time

url = "https://comment.kuwo.cn/com.s"

# 定义请求参数
params = {
    "type": "get_comment",
    "f": "web",
    "page": "1",
    "rows": "5",
    "digest": "2",
    "sid": "93",
    "uid": "0",
    "prod": "newWeb",
    "httpsStatus": 1,
    "reqId": "de3bd9d0-5da7-11ee-be91-09b4fcdf5e69",
    "plat": "web_www",
}

for page in range(3):
    params["page"] = str(page + 1)
    res = requests.get(url=url, params=params)
    res_dict = res.json()
    comments = res_dict["rows"]

    # 循环遍历每条评论并打印出来
    print("---第{}页评论---".format(page))
    for comment in comments:
        print(comment["msg"])

#
#
# import requests
#
# url = "https://comment.kuwo.cn/com.s"
#
# # 定义请求参数
# params = {
#     "type": "get_comment",
#     "f": "web",
#     "page": "3",
#     "rows": "5",
#     "digest": "2",
#     "sid": "93",
#     "uid": "0",
#     "prod": "newWeb",
#     "httpsStatus": 1,
#     "reqId": "de3bd9d0-5da7-11ee-be91-09b4fcdf5e69",
#     "plat": "web_www",
# }
#
# my_headers = {
#     "Referer": "https://www.kuwo.cn/",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
# }
#
# res = requests.get(url=url, params=params, headers=my_headers)
# res_dict = res.json()
# # print(res_dict)
# comments = res_dict["rows"]
#
# for comment in comments:
#     print(comment["msg"])
