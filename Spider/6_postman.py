# import requests
#
# res = requests.get("https://s.weibo.com/weibo?q=%E5%B0%8F%E8%B1%A1%E5%AD%A6%E9%99%A2")
#
# print(res.text)

import requests

url = "https://movie.douban.com/"

payload = {}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Cookie': 'll="108296"; bid=Woamus9T00o; _pk_id.100001.4cf6=bf354f2cf61a34f4.1694691318.; __utmz=30149280.1694691319.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmz=223695111.1694691319.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=DB61EB1C0F832994174DF0017317B48DE|7841d7aa8f0a2d47b0a49f9bf25eea6d; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.1642716311.1694691319.1694765712.1696409609.5; __utmb=30149280.0.10.1696409609; __utmc=30149280; __utma=223695111.107045083.1694691319.1694766000.1696409609.5; __utmb=223695111.0.10.1696409609; __utmc=223695111',
  'Host': 'movie.douban.com',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',

}

response = requests.get(url, headers=headers)
response.encoding = "utf-8"

print(response.text)


