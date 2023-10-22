# import requests
# import bs4
#
# res = requests.get("https://so.gushiwen.org/shiwen")
# res.encoding = "utf-8"
#
# soup = bs4.BeautifulSoup(res.text, "lxml")
# print(type(soup))


# import requests
# import bs4
#
# res = requests.get("https://so.gushiwen.org/shiwen")
# res.encoding = "utf-8"
#
# soup = bs4.BeautifulSoup(res.text, "lxml")
# print(type(soup))
# print("title标签：", soup.title)
# print("soup.title的类型：", type(soup.title))
# print("标签内的内容：", soup.title.getText())


# import requests
# import bs4
#
# res = requests.get("https://www.suning.com")
# res.encoding = "utf-8"
#
# soup = bs4.BeautifulSoup(res.text, "lxml")
# print(type(soup))
# print("title标签：", soup.title)
# print("soup.title的类型：", type(soup.title))
# print("标签内的内容：", soup.title.getText())


# import requests
# import bs4
#
# res = requests.get("https://so.gushiwen.org/shiwen")
#
# with open("./tmp/shiwen.html", "wb") as file:
#     file.write(res.content)
#
# html_file = open("./tmp/shiwen.html", encoding="utf-8")
# soup = bs4.BeautifulSoup(html_file, "lxml")
# print("title标签：", soup.title)
# print("soup.title的类型", type(soup.title))
# print("标签内的内容：", soup.title.getText())


# import requests
# import bs4
#
# res = requests.get("https://so.gushiwen.org/shiwen")
# res.encoding = "utf-8"
#
# soup = bs4.BeautifulSoup(res.text, "lxml")
# a_tag = soup.select("a")
# print("a标签数量：", len(a_tag))
# print("a标签内容：")
# print(a_tag)


# import requests
# import bs4
#
# res = requests.get("https://so.gushiwen.org/shiwen")
# res.encoding = "utf-8"
#
# soup = bs4.BeautifulSoup(res.text, "lxml")
# a_tag = soup.select("a")
# a_100 = a_tag[99]
# print("第100个a标签：", a_100)
# print("第100个a标签的属性值：", a_100['href'])



# import requests
# import bs4
#
# res = requests.get("http://www.suning.com")
#
# with open("./tmp/suning.html", "wb") as file:
#     file.write(res.content)
#
# html_file = open("./tmp/suning.html", encoding="utf-8")
# soup = bs4.BeautifulSoup(html_file, "lxml")
# print(soup.select("body > div.index-header > div.ng-header-con > div.ng-header-box > a > img"))
# tag = soup.select("body > div.index-header > div.ng-header-con > div.ng-header-box > a > img")
# img_url = "http:" + tag[0]["src"]
#
# result = requests.get(img_url)
# with open("./tmp/suning_img.png", "wb") as file:
#     file.write(result.content)



# import requests
# import bs4
#
# res = requests.get("http://www.suning.com")
#
# with open("./tmp/suning.html", "wb") as file:
#     file.write(res.content)
#
# html_file = open("./tmp/suning.html", encoding="utf-8")
# soup = bs4.BeautifulSoup(html_file, "lxml")
# tag_list = soup.select(".index-list a")
# # print(tag_list)
#
# for tag in tag_list:
#     print(tag.getText())









