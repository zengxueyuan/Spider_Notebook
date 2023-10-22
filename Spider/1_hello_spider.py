# 1.
# import requests
#
# res = requests.get("https://so.gushiwen.cn/shiwen/")
# print("返回码：", res.status_code)


# 2.
# import requests
#
# res = requests.get("https://so.gushiwen.cn/shiwen/")
# res.encoding = "utf-8"  # 防止乱码
#
# print("返回内容：", res.text)
# print("结果类型：", type(res))
# print("返回码：", res.status_code)


# # 3.
# import requests
#
# res = requests.get("https://so.gushiwen.cn/shiwen/")
# res.encoding = "utf-8"
# # 写入二进制内容，用wb
# with open("./tmp/shiwen.html", "wb") as file:
#     file.write(res.content)  # content把response对象转换为二进制数据

# 4.
import requests

res = requests.get("https://so.gushiwen.org/mingju")
res.encoding = "utf-8"

with open("./tmp/mingju.html", "wb") as file:
    file.write(res.content)
