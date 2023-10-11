

# 爬虫 Spider

## 认识爬虫

爬虫（web crawler）自动抓取万维网信息的程序或者脚本

- 浏览器向服务器发起请求，服务器给予响应。先请求，后相应
- 网页只是一个小二（中介），反馈信息在**服务器**

1. #### <u>爬虫工作原理</u>

- 获取数据
- 解析数据
- 提取数据
- 存储数据

2. #### <u>requests模块</u>

```python
import requests

res = requests.get("https://so.gushiwen.cn/shiwen/")
print("返回码：", res.status_code)
```

返回码： 200

```python
import requests

res = requests.get("https://so.gushiwen.cn/shiwen/")
res.encoding = "utf-8"  # 防止乱码

print("返回内容：", res.text)
print("结果类型：", type(res))
print("返回码：", res.status_code)
```

结果类型： <class 'requests.models.Response'>
返回码： 200

```python
import requests

res = requests.get("https://so.gushiwen.cn/shiwen/")
res.encoding = "utf-8"
# 写入二进制内容，用wb
with open("./tmp/shiwen.html", "wb") as file:
    file.write(res.content)  # content把response对象转换为二进制数据
```

- 可能会疑惑为什么不直接写入res.text文本，而是写入res.content二进制数据呢？

因为`res.text`是为了方便直观查看返回的数据内容，但你会发现这些内容里有大量的页面代码，这并不是我们最终想要的数据。而`res.content`将这些数据内容转换成电脑更容易读懂的二进制数据是为了方便后面的解析数据。

3. #### <u>Robots协议</u>

1） 搜索技术应服务于人类，同时尊重信息提供者的意愿，并维护其隐私权；

2）网站有义务保护其使用者的个人信息和隐私不被侵犯。

正如知名专栏作家DannySullivan所言，robots协议是规范搜索引擎爬虫行为的极少数约定之一，理应遵守，它不仅仅让整个互联网的开放性变成可能，最终也让整个互联网用户受益。

### <u>总结</u>

![image-20230927111431846](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230927111431846.png)



# HTML

超文本标记语言HTML（HyperText Markup Language）

- 由**标签**和**文本**组成的HTML文档，再通过**属性**引入欸话页面的信息

### 总结

![image-20230928091227344](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230928091227344.png)



# BeautifulSoup

### 创建对象

```python
import requests
import bs4

res = requests.get("https://so.gushiwen.org/shiwen")
res.encoding = "utf-8"

soup = bs4.BeautifulSoup(res.text, "lxml")
print(type(soup))
```

- 第一个参数`res.text`就是获取的页面信息，表示BeautifulSoup对象soup后面的一系列操作都是在这个页面的基础上进行解析。

- 而第二个参数`'lxml'`其实是一个**解析器**，你可以将它理解成BeautifulSoup这个工具的能量来源。



### 解析页面

```python
import requests
import bs4

res = requests.get("https://so.gushiwen.org/shiwen")
res.encoding = "utf-8"

soup = bs4.BeautifulSoup(res.text, "lxml")
print(type(soup))
print("title标签：", soup.title)
print("soup.title的类型：", type(soup.title))
print("标签内的内容：", soup.title.getText())
```

`<class 'bs4.BeautifulSoup'>`
`title标签： <title>`
`古诗文大全_古诗文网
</title>
soup.title的类型： <class 'bs4.element.Tag'>
标签内的内容： 
古诗文大全_古诗文网`



### 处理HTML文件

```python
import requests
import bs4

res = requests.get("https://so.gushiwen.org/shiwen")

with open("./tmp/shiwen.html", "wb") as file:
    file.write(res.content)

html_file = open("./tmp/shiwen.html", encoding="utf-8")
soup = bs4.BeautifulSoup(html_file, "lxml")
print("title标签：", soup.title)
print("soup.title的类型", type(soup.title))
print("标签内的内容：", soup.title.getText())
```

`title标签： <title>`
`古诗文大全_古诗文网
</title>
soup.title的类型 <class 'bs4.element.Tag'>
标签内的内容： 
古诗文大全_古诗文网`

可以发现显示的信息和直接操作返回结果的打印信息是一样。也就说明BeautifulSoup正常处理了HTML文件里的信息。

<u>当我们通过爬虫请求爬取了大量的网页文件之后，在需要时再去使用BeautifulSoup处理这些HTML文件</u>。



#### select()

```python
import requests
import bs4

res = requests.get("https://so.gushiwen.org/shiwen")
res.encoding = "utf-8"

soup = bs4.BeautifulSoup(res.text, "lxml")
a_tag = soup.select("a")
print("a标签数量：", len(a_tag))
print("a标签内容：")
print(a_tag)
```



```python
import requests
import bs4

res = requests.get("https://so.gushiwen.org/shiwen")
res.encoding = "utf-8"

soup = bs4.BeautifulSoup(res.text, "lxml")
a_tag = soup.select("a")
a_100 = a_tag[99]
print("第100个a标签：", a_100)
print("第100个a标签的属性值：", a_100['href'])
```

`第100个a标签： <a href="https://so.gushiwen.cn/shiwen/default_2Aa6acb3e3e0ddA1.aspx">贯休</a>`
`第100个a标签的属性值： https://so.gushiwen.cn/shiwen/default_2Aa6acb3e3e0ddA1.aspx`



#### 选择器

抓取苏宁易购首页上的一张图片

```python
import requests
import bs4

res = requests.get("http://www.suning.com")

with open("./tmp/suning.html", "wb") as file:
    file.write(res.content)

html_file = open("./tmp/suning.html", encoding="utf-8")
soup = bs4.BeautifulSoup(html_file, "lxml")
print(soup.select("body > div.index-header > div.ng-header-con > div.ng-header-box > a > img"))
tag = soup.select("body > div.index-header > div.ng-header-con > div.ng-header-box > a > img")
img_url = "http:" + tag[0]["src"]

result = requests.get(img_url)
with open("./tmp/suning_img.png", "wb") as file:
    file.write(result.content)
```



#### 获取苏宁易购商品分类信息

```python
import requests
import bs4

res = requests.get("http://www.suning.com")

with open("./tmp/suning.html", "wb") as file:
    file.write(res.content)

html_file = open("./tmp/suning.html", encoding="utf-8")
soup = bs4.BeautifulSoup(html_file, "lxml")
tag_list = soup.select(".index-list a")
# print(tag_list)

for tag in tag_list:
    print(tag.getText())
```



### 总结

![image-20230928100350209](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230928100350209.png)









# Async_data_load

- 爬取酷我评论

#### Network

```python
import requests

res = requests.get("https://www.kuwo.cn/rankList")

with open("./tmp/热歌榜.html", "wb") as file:
    file.write(res.content)
```

会发现，具体的评论内容并不在这个请求得到结果之中

- 检查Preview，发现根本没有评论

  

### XHR

全称：XMLHttpRequest

- 用于**异步网页数据请求**：指这个网络请求不是在第一条打开网页的请求发起的同时进行的，而是在页面框架已经被浏览器加载出来的时候，通过另一个请求获取具体的内容

- 不更改浏览器地址栏上的地址前提下，<u>局部地刷新页面</u>

  

### JSON

```python
import requests

res = requests.get("https://comment.kuwo.cn/com.s?type=get_rec_comment&f=web&page=1&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=622e42d1-5da5-11ee-89ac-db57de720abf&plat=web_www&from=")
res_dict = res.json()
comments = res_dict["rows"]

for comment in comments:
    print(comment["msg"])
```

`许嵩有十多首歌曲都在飙升榜前列`
`希望魔卡少女樱透明牌的歌的再一次登上去的点赞，让我看看有多少人是樱粉，记得举起你们的小手手呦~ ^_^，在这里点赞———>
脚踏实地谋发展 努力努力再努力x
我最丑-_-求个关注不过分吧[鲜花]`
`三辑冲呀`



### 总结

![image-20230928102437516](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230928102437516.png)





# More_pages

### 参数

- **GET**请求中，额外的信息放在请求地址后面，跟着符号**？**后，定义方式为**参数名=参数值**（type=get_comment），type为参数，get_comment为值
- 不同参数用**&**隔开

```python
import requests

# url = "https://comment.kuwo.cn/com.s?type=get_comment&f=web&page=2&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=1b3d5530-5da7-11ee-aa8b-df339d740a53&plat=web_www&from="
res = requests.get("https://comment.kuwo.cn/com.s?type=get_comment&f=web&page=3&rows=5&digest=2&sid=93&uid=0&prod=newWeb&httpsStatus=1&reqId=f2b904b0-5da6-11ee-aa8b-df339d740a53&plat=web_www&from=")
res_dict = res.json()
comments = res_dict["rows"]

for comment in comments:
    print(comment["msg"])
```

会发现只是参数`page=3`的区别

- 这样显得整个地址字符串特别冗长，代码阅读和修改都显得麻烦 

#### 参数的定义

```python
import requests

url = "https://comment.kuwo.cn/com.s"

# 定义请求参数
params = {
    "type": "get_comment",
    "f": "web",
    "page": "3",
    "rows": "5",
    "digest": "2",
    "sid": "93",
    "uid": "0",
    "prod": "newWeb",
    "httpsStatus": 1,
    "reqId": "de3bd9d0-5da7-11ee-be91-09b4fcdf5e69",
    "plat": "web_www",
}

res = requests.get(url, params=params)
```

写入`params`是一样的效果！url的**`?`后面**



#### 请求多页

```python
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
```



### 请求头 Request Headers

**`Referer` **：表示发起当前这条网络请求之前，访问的是什么地址

`User-Agent`: 记录了发起网络请求的浏览器的信息

- url表示请求资源
- params表示请求指定信息
- 请求头包含和用户身份及行为相关的内容



### 总结

![image-20230928185532827](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230928185532827.png)







# Postman

### Elements

- Expand recursively
- Scroll into view

`elements`被放在所有标签页的第一个，因为对于了解HTML代码与页面之间的关系最为直接，也是前端工程师以及爬虫编写者最常用的功能之一。

### Console

- 一个可以在浏览器页面上执行**JavaScript**代码，比如修改页面的一些内容、属性等
- 对于某些爬取，需要模拟用户的行为（输入账号密码等），这时候需要**JavaScript**
- **Console**是一个验证**JavaScript**代码正确性的地方
- `document.querySelector()` 可以用来挑选元素

### Network

- `All` 标签会显示所有的网络请求
- `XHR` 显示所有为了**动态加载内容**而发送的请求
- 1. Preserve log：刷新页面，之前抓取的网络消息不会被清空
     - 可以让网络请求记录一直保留下来，老的记录不会在刷新页面或者跳转的时候被删除，方便联系多个操作，从一开始分析网络交互的过程
  2. Slow 3G：让浏览器模拟网络状况较差的情况
     - 网页开发工程师为了模拟网络较差情况，以验证自己开发的网页功能正常
     - 可以借助这个功能验证网页内容中哪些是异步加载的

### Application

- **`Storage`** : 保存在计算机本地的一些信息
  - **`Cookies`**: 存储小，有过期限制
  - **`Local Storage`**
  - **`Session Storage`**

### Postman

- 强大的网页调试与发送网页HTTP请求的工具

- 我们通过爬虫之前，希望验证一下发送的某些网络请求是否能起到我们预想的效果，可以借助Postman

  **爬虫工程师模拟和验证网络请求的神器Postman**

  1. 自动生成python请求代码
  2. 构造headers信息（`Headers`->`Bulk edit`）

- 自动接获信息

  - Chrome浏览器的插件方式进行安装（后续自行使用）

### 总结

![image-20230929002220636](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230929002220636.png)