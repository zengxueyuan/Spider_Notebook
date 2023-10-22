# 1.
import requests

url = "https://www.xiaoxiangxueyuan.com/pages/s1/joke.html"
res = requests.get(url)
res.encoding = "utf-8"
print(res.text)