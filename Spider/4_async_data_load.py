# import requests
#
# res = requests.get("https://www.kuwo.cn/rankList")
#
# with open("./tmp/热歌榜.html", "wb") as file:
#     file.write(res.content)


import requests

res = requests.get("https://comment.kuwo.cn/com.s?type=get_rec_comment&f=web&page=1&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=622e42d1-5da5-11ee-89ac-db57de720abf&plat=web_www&from=")
res_dict = res.json()
comments = res_dict["rows"]

for comment in comments:
    print(comment["msg"])
