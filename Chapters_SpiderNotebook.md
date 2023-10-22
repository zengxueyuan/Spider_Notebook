

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

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230929002220636.png" alt="image-20230929002220636" style="zoom:67%;" />





# csv_excel

**CSV** 全称Comma-Separated Values

```python
file = open("./tmp/data.csv", "w")
file.write("哪吒,姜子牙,花木兰")
file.close()
```

用csv格式保存数据，读写比较方便，易于实现，文件也比较小

### **csv模块** 

```python
import csv

with open(r"./tmp/book.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["斗破苍穹", "天蚕土豆"])
```

- `newline=""` 是避免csv文件出现两倍行距，避免表格的行与行之间出现空白行的情况

- `writerow()` 方法每次向文件写入一行内容，想要多次写入需要多次调用；并且传入**列表** 

#### 读取csv文件

```python
import csv

with open(r"./tmp/book.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

#### 保存苏宁易购商品分类信息

```python
import requests
import bs4
import csv

# 发起网页请求，用BeautifulSop解析HTML
res = requests.get("https://www.suning.com")

with open("./tmp/suning.html", "wb") as file:
    file.write(res.content)

html_file = open("./tmp/suning.html", encoding="utf-8")
soup = bs4.BeautifulSoup(html_file, "lxml")

# 使用csv文件储存信息
with open(r"./tmp/商品分类.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    goods_list = []
    tag_list = soup.select(".index-list a")
    for tag in tag_list:
        goods_list.append(tag.getText())
    writer.writerow(goods_list)
```

### **openpyxl模块**

```python
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "new_title"

wb.save(r"./tmp/first.xlsx")
```

- `Workbook`是一个工作簿
- `wb.active`获取当前工作表，将获取到的工作表赋值给`sheet`，通常指第一张工作表`sheet1`
- `sheet.title`赋值表名

##### 文件操作 

1. 写入内容

```python
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "new_title"

sheet['A1'].value = "酷我音乐"

wb.save(r"./tmp/first.xlsx")
```

2. 读取内容

```python
import openpyxl
wb = openpyxl.load_workbook("./tmp/first.xlsx")
sheet = wb['new_title']
print(sheet['A1'].value)
```

3. 一次性读取

```python
import openpyxl

wb = openpyxl.load_workbook("./tmp/my_excel.xlsx")

sheet_list = wb.sheetnames

for sheet_name in sheet_list:
    sheet = wb[sheet_name]

    for i in range(1, sheet.max_row + 1):
        print(sheet['A' + str(i)].value)
```

##### 保存酷我音乐评论

```python
import requests
import time
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
row_num = 1

url = "https://comment.kuwo.cn/com.s"

# 定义请求参数
my_params = {
    "type": "get_comment",
    "f": "web",
    "rows": "20",
    "digest": "2",
    "sid": "93",
    "uid": "0",
    "prod": "newWeb",
    "httpsStatus": 1,
    "reqId": "de3bd9d0-5da7-11ee-be91-09b4fcdf5e69",
    "plat": "web_www",
}

# 定义请求头
my_headers = {
    "Referer": "https://www.kuwo.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
}

# 爬取
for page in range(3):
    print("===爬取第{}页===".format(page + 1))
    my_params['page'] = page + 1
    res = requests.get(url, params=my_params, headers=my_headers)

    res_dict = res.json()
    comments = res_dict["rows"]

    for comment in comments:
        sheet['A' + str(row_num)].value = comment['msg']
        row_num += 1

    time.sleep(2)

wb.save("./tmp/酷我音乐评论.xlsx")
print("保存成功")
```

### 总结

![image-20230929112204936](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20230929112204936.png)

# MySQL

**MySQL 从删库到跑路~~~**

- MySQL数据库，中文名称关系型数据库管理系统，由瑞典MySQL AB公司开发，属于Oracle旗下产品
- MySQL是一个数据管理系统，系统由很多张表组成，表里面是我们存放的具体数据。而访问这些表需要和数据库的交流语言-SQL语言

### 数据库的连接

在Python中专门用来与MySQL数据库进行连接的模块，称之为**`pymysql模块`** 

```python
import pymysql

# 打开数据库连接
db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901', database='study', charset='utf8', port=3306)
# 使用cursor方法获取操作游标
cursor = db.cursor()
# 关闭光标对象
cursor.close()
# 关闭数据库链接
db.close()
print("连接成功！")
```

`host`：数据库的地址，这里使用的是阿里云的数据库

`user`：用户名

`passwd`：密码

`database`：数据库名

`charset`：使用utf-8作为编码格式

### 数据库中建表

```python
import pymysql

# 打开数据库连接
db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901', database='study', charset='utf8', port=3306)
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 如果STUDENT表存在，就删除
cursor.execute(("DROP TABLE IF EXISTS STUDENT"))
# 定义要执行的SQL语句
sql = """
    CREATE TABLE STUDENT(
        NAME CHAR(20),
        AGE INT,
        SEX CHAR(1))
"""
# 执行SQL语句
cursor.execute(sql)
# 提交数据
db.commit()
# 关闭光标对象
cursor.close()
# 关闭数据库连接
db.close()

print("CREATE TABLE OK")
```

### 常用的SQL语句

#### 插入数据

```python
import pymysql

# 打开数据库连接
db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901',
                     database='study', charset='utf8', port=3306)
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 如果STUDENT表存在，就删除
cursor.execute(("DROP TABLE IF EXISTS STUDENT"))
# 定义要执行的SQL语句
sql = """
    CREATE TABLE STUDENT (
        NAME CHAR(20),
        AGE INT,
        SEX CHAR(1)
    )
"""
# 执行SQL语句
cursor.execute(sql)

# 定义要执行的插入数据的SQL语句
insert_sql = "INSERT INTO STUDENT (NAME, AGE, SEX) VALUE (%s, %s, %s)"
data = [("july", 17, "F"), ("jane", 18, "F"), ("jack", 20, "M")]
# 执行SQL语句
cursor.executemany(insert_sql, data)
# 提交数据
db.commit()

# 关闭光标对象
cursor.close()
# 关闭数据库连接
db.close()

print("insert ok")
```

#### 查询数据

```python
import pymysql

db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS STUDENT")

sql = """
    CREATE TABLE STUDENT (
        NAME CHAR(20),
        AGE INT,
        SEX CHAR(1)
    )
"""
cursor.execute(sql)
insert_sql = "INSERT INTO STUDENT(NAME, AGE, SEX) VALUE (%s, %s, %s)"
data = [("july", 17, "F"), ("jane", 18, "F"), ("jack", 20, "M")]
cursor.executemany(insert_sql, data)
db.commit()

# 定义要执行的查询数据的sql语句
query_sql = "SELECT * FROM STUDENT"
# 使用execute()方法执行sql语句
cursor.execute(query_sql)
# 使用fetchall()获取全部数据
res = cursor.fetchall()
# 打印获取的数据
print(res)

cursor.close()
db.close()
```

`SELECT * FROM TABLE`是常用的查询**整个**TABLE表的命令，这里的`TABLE`是表名的统称，我们要将`TABLE`替换成具体需要查询的表名，例如代码中替换成了`STUDENT`。

接下来要使用`cursor`调用`fetchall()`方法去获取**全部数据**，并将返回值赋值给`res`。

| 方法         | 含义           |
| :----------- | :------------- |
| fetchone()   | 获取一行数据   |
| fetchmany(3) | 获取前三行数据 |
| fetchall()   | 获取全部数据   |

### 将酷我音乐评论保存到数据库中

#### 创建music表

```PYTHON
import pymysql

db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS MUSIC")
sql = """
    CREATE TABLE MUSIC (
        COMMENT CHAR(225)
    )
"""
cursor.execute(sql)
db.commit()
cursor.close()
db.close()
print("CREATE TABLE OK")
```

#### 插入评论数据

将之前我们爬取酷我音乐评论的代码封装成`get_info()`函数保存在`music`文件中。从`music`文件中导入`get_info()`函数并调用：

`music.py`

```python
import requests

def get_info():

    url = "https://comment.kuwo.cn/com.s"
    data_comments = []

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
        print("---第{}页评论---".format(page + 1))
        for comment in comments:
            data_comments.append(comment["msg"])
            
    return data_comments
```

```python
from music import get_info

data = get_info()
print(data)
```

结合起来

```python
import pymysql
from music import get_info

db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS MUSIC")
sql = """
    CREATE TABLE MUSIC (
        COMMENT CHAR(225)
    )
"""
cursor.execute(sql)
print("CREATE TABLE OK")

# 插入评论数据
insert_sql = "INSERT INTO MUSIC(COMMENT) VALUES (%s)"
data = get_info()
cursor.executemany(insert_sql, data)
db.commit()

cursor.close()
db.close()
print("insert ok")
```

#### 查看数据

```python
import pymysql
from music import get_info

db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS MUSIC")

sql = """
    CREATE TABLE MUSIC (
        COMMENT CHAR(255)
    )
"""
cursor.execute(sql)
insert_sql = "INSERT INTO MUSIC (COMMENT) VALUES (%s)"
data = get_info()
cursor.executemany(insert_sql, data)
db.commit()

# 查看数据
query_sql = "SELECT * FROM MUSIC"
cursor.execute(query_sql)
res = cursor.fetchall()
print(res)

cursor.close()
db.close()
```

### 总结

![image-20231004200818898](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231004200818898.png)



# Selenium

相对于使用`requests`模块，`selenium`模块更真实的模拟了一个人的操作，不容易被屏蔽

#### 使用selenium启动浏览器

```python
from selenium import webdriver

browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
browser.get("https://www.suning.com/")
```

- 从**selenium**导入`webdriver`，是之后用作浏览器驱动器的引擎包
- `executable_path`定义的是一个文件的地址，这个文件是预先下载好的浏览器驱动程序，通过它的支持才能操纵浏览器

![image-20231002155031307](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231002155031307.png)

#### 无界面模式

我们需要使用**无界面模式**来解决这个问题。所谓**无界面模式**，就是**selenium**在启动浏览器的时候，不需要启动它的图形界面，只是使用浏览器的核心功能，完成对用户操作动作的响应、向网络发起请求和获得结果等。

Chrome（谷歌）和Firefox（火狐）浏览器，都支持无界面模式（也叫无头模式）；Linux与火狐浏览器结合最好，所以选择了火狐浏览器与selenium配合。

- "--headless"：无界面模式
- 指定驱动 geckodriver
- 由于浏览器启动一般需要耗费一点时间，为了保证加载完成之后在进行访问，使用`time.sleep(2)`等待两秒
- 在调用`browser.get()`后，通过`browser.page_source`可以获得页面的HTML内容，并`print()`出来
- 在无界面方法下，看不到它的样子，但可以拍快照并存储 `browser.save_screenshot()`，可以直观打开页面当前的模样（无界面）

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

browser_options = Options()
browser_options.add_argument("--headless")

browser = webdriver.Firefox(executable_path="data/geckodriver.exe", options=browser_options)
# 等待两秒，保证浏览器加载完成
time.sleep(2)

browser.get("https://www.suning.com/")
# 获取HTML内容并打印
html = browser.page_source
print(html)

# 保存页面截图
browser.save_screenshot("tmp/suning_screenshot.png")

browser.quit()
```

#### 在页面中定位元素

| 方法名                                          | 得到结果                                                |
| :---------------------------------------------- | :------------------------------------------------------ |
| browser.find_element_by_class_name(name)        | 根据class属性查找一个元素                               |
| browser.find_elements_by_class_name(name)       | 根据class属性查找符合条件的元素列表                     |
| browser.find_element_by_css_selector(selector)  | 根据选择器（我们学习BeautifulSoup时提到的）查找一个元素 |
| browser.find_elements_by_css_selector(selector) | 根据选择器查找符合条件的元素列表                        |
| browser.find_element_by_id(id)                  | 根据元素id查找                                          |
| browser.find_elements_by_id(id)                 | 根据id查找元素列表                                      |
| browser.find_element_by_tag_name(name)          | 根据标签名查找一个元素                                  |
| browser.find_elements_by_tag_name(name)         | 根据标签名查找元素列表                                  |
| browser.find_element_by_link_text(text)         | 根据a标签的链接查找一个元素                             |
| browser.find_elements_by_link_text(text)        | 根据a标签的链接查找元素列表                             |

获取网页文本、创建对象对内容进行解析、提取其中的信息。

这三个操作步骤，使用**selenium**跟使用 **requests** + **BeautifulSoup** 有很多相似之处。

![image-20231005154421346](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231005154421346.png)

- 缺点：使用**selenium**获取网页内容时，明显感觉比`requests.get()
  - 这是因为每次进行网页请求，都需要重启浏览器，与`requests.get()`直接调用网络借口进行访问的性能是没法比较的
- 优点：用于模拟人类的交互式网页操作

#### 填写表单

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

browser_options = Options()
browser_options.add_argument("--headless")

browser = webdriver.Firefox(executable_path="data/geckodriver.exe", options=browser_options)

# 等待两秒，保证浏览器加载完成
time.sleep(2)

browser.get("https://www.suning.com/")

# 查找搜索框元素并输入关键字
search_box = browser.find_element_by_css_selector("#searchKeywords")
search_box.send_keys("手机")

# 等待两秒，保证搜索结果加载完成
time.sleep(2)

# 获取HTML内容并打印
html = browser.page_source
print(html)

# 保存页面截图
browser.save_screenshot("tmp/screen_shot.png")

browser.quit()
```

通过调用`element`的`send_keys()`方法，在搜索框中填入**手机**，通过screenshot来查看结果。

#### 点击按钮

```python
from selenium import webdriver
import time

browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
time.sleep(1)

browser.get("https://www.suning.com/")

# 查找搜索框元素并输入关键字
search_box = browser.find_element_by_css_selector("#searchKeywords")
search_box.send_keys("手机")

# 查找搜索按钮元素并点击
search_button = browser.find_element_by_css_selector("#searchSubmit")
search_button.click()

# 等待两秒，保证搜索结果加载完成
time.sleep(2)

browser.quit()
```

### 爬取苏宁信息

#### 滚动页面

- 进行分页加载时，可以通过**Slow3G**看网页加载情况
  - 由于苏宁一页中商品内容比较多，服务器第一次返回的只是部分内容，需要用户不停滚动页面，发送新的请求，取回剩下的页面内容
- **JavaScript**可以控制浏览器实现滚动效果
  - 向浏览器传入一段JavaScript代码 `window.scrollTo(0, document.body.scrollHeight)`
- `browser.execute_script()`完成滚动到页面底部的动作

```python
from selenium import webdriver
import time

browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
time.sleep(2)

# 访问页面
browser.get("https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html?safp=d488778a.homepagev8.126605238627.65&safc=cate.0.0&safpn=10001")

# 将页面滚动到底部
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# 获取页面快照
ret = browser.save_screenshot("tmp/huawei.png")
print("快照拍摄结果：", ret)
time.sleep(2)

browser.quit()
```

#### 等待加载

- 所谓等待加载，就是等到某些内容被浏览器读取。本案例中，就是等待所有内容都被网页访问者看到。
  - 通过人工查看的方式，可以发现在该信息页面中，每页会出现120个商品结果

- 仔细分析页面中的商品项，每个商品信息都由一个class是**item-wrap**的标签包围起来。因此，当出现120个商品时，页面中就会有120个**item-wrap**项。

- 于是，我们的循环逻辑是，等待两秒钟，通过`browser.find_elements_by_class_name('item-wrap')`获取页面中class名字是`'item-wrap'`的元素列表，放到变量`item_wraps`中。然后通过`len(item_wraps)`方法计算一下`item_wraps`的元素个数`wrap_len`。

#### 提取信息

BeautifulSoup 解析代码

```python
from selenium import webdriver
import time
import bs4

# ==== BeautifulSoup ====
def products_info():
    print("获取商品信息：")
    # 读取HTML页面
    html = browser.page_source
    # 加载页面内容
    soup = bs4.BeautifulSoup(html, "lxml")
    items = soup.select(".title-selling-point")
    # 遍历商品信息
    for item in items:
        print("======")
        print(item.text.strip())
        
# ==== Selenium ====
def products_info():
    print("获取商品信息：")
    items = browser.find_elements_by_class_name("title-selling-point")
    for item in items:
        print("=====")
        print(item.text)


browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
time.sleep(2)

browser.get(
    "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html?safp=d488778a.homepagev8.126605238627.65&safc=cate.0.0&safpn=10001")

# 将页面滚动到底部
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

item_wraps = browser.find_elements_by_class_name('item-wrap')

while len(item_wraps) < 120:
    # 将页面滚动到底部
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    item_wraps = browser.find_elements_by_class_name('item-wrap')
    # print(len(item_wraps))

    time.sleep(2)

# 调用函数获取相关信息
products_info()

browser.quit()
```

#### 点击下一页

```python
next_page_button = browser.find_element_by_id("nextPage")
next_page_button.click()
```

这里在页面中定位下一页按钮元素的方法不只一种，既可以这样通过元素id定位，也可以在开发者工具中使用**Copy Selector**获得元素的选择器，然后通过`browser.find_element_by_css_selector()`方法把元素找出来。

#### 获取多页

```python
from selenium import webdriver
import time

# ==== Selenium ====
def products_info():
    print("获取商品信息：")
    items = browser.find_elements_by_class_name("title-selling-point")
    for item in items:
        print("=====")
        print(item.text)


def get_page():
    item_wraps = []
    while len(item_wraps) < 120:
        # 将页面滚动到底部
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        item_wraps = browser.find_elements_by_class_name('item-wrap')
        time.sleep(2)

    # 获取相关信息
    products_info()

    # 下一页
    next_page_button = browser.find_element_by_id("nextPage")
    next_page_button.click()

    
browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
time.sleep(2)

browser.get(
    "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html?safp=d488778a.homepagev8.126605238627.65&safc=cate.0.0&safpn=10001")

# 获取三页数据
for i in range(3):
    get_page()
    time.sleep(2)

browser.quit()
```

### 总结



![image-20231008174913381](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231008174913381.png)



# Cookie

解决登录问题的武器就是**cookie**和**session**

#### http协议无状态

- 我们请求的服务器都只有1秒记忆，响应一旦结束，服务器就忘记该”人“
- 由于**http**请求无状态的特征，为了能够追踪识别用户身份，人类发明了**cookie**

### cookie

#### cookie原理

1. 浏览器首次请求访问某服务器
2. 服务器接受请求，生产cookie信息
3. 服务器的响应返回客户端时（Response），会将cookie一并带回，并写入浏览器
4. 在此使用浏览器访问该服务器时，浏览器会自动携带cookie信息发起请求
5. 服务器读取cookie信息，识别出这个请求时原来的浏览器发出，做出相应

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231008175551108.png" alt="image-20231008175551108" style="zoom: 80%;" />

#### cookie简介

- 由服务器生成，存储在浏览器客户端的一块小数据
- cookie的长度：不超过4KB
- cookie的格式：`key:value`
- cookie的时效：由服务器设定过期时间，默认一个<u>会话</u>（可以理解为浏览器从打开到关闭的时间）

#### cookie的场景

​	”记住我“  ”下次自动登录“

### 模拟登录

```python
import requests

# 书单页面连接
url = "https://www.kanman.com/api/getuserinfobook?product_id=1&productname=kmh&platformname=pc&page=1&user_id=260809114&refresh=true&_=1696761852430"

# headers中的Cookie值需要手动在浏览器中登录之后根据实际情况进行替换
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
    "Referer": "https://www.kanman.com/uc/booklist.html",
    "Cookie": "koa:sess=ca2a17fe-c162-425f-8894-74b275914c90; koa:sess.sig=HFlx7pq3Cxrq4I0dkpmkvLMHbqo; user=%7B%22Uid%22%3A260809114%2C%22openid%22%3A%2223305584_369D3EDB2C0AD29D5B9EB3328BB678C9%22%2C%22type%22%3A%22mkxq%22%2C%22token%22%3A%221134a4c4e8ce0adeff87170ede79e2d4d6f39b2290085ea26b57da12cfac60be%22%7D; user.sig=N6D7dfpzmTAYi9DYGLcF0O1ELs8",
}

# 请求结果并转换成JSON格式
res = requests.get(url, headers=headers)
json_data = res.json()

# 打印书单中的每部漫画的标题
for comic_info in json_data["data"]["book_list"][0]["comic_info"]:
    print(comic_info["comic_name"])
```

> 手动输入账户信息登陆后直接复制cookie
>
> - 优点：简单粗暴有效
> - 缺点：cookies一旦失效，需再次登录复制，代码可用性大打折扣

**方案二：模拟登录，动态获取**

- **GET**一般用于<u>从服务器获取数据</u>，它的请求参数我们在地址栏清晰可见，安全性较低
- **POST**一般用于<u>向服务器发送数据</u>，它的请求参数不在地址栏显示，安全性较高

在做登录验证的时候，涉及到用户的隐私信息，绝大部分网站使用**POST**请求

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231008212719740.png" alt="image-20231008212719740" style="zoom:50%;" />

```python
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

res = requests.post(url, headers=headers, data=data)

# 获取cookie信息，以备后续使用
cookies = res.cookies
print("请求首页返回的cookie", cookies)
print("首次连接建立后，服务器会生成cookie信息，跟随响应返回浏览器...此时，我已经拿到cookies信息啦！")

# 让程序随机睡2到5秒，逼真地模仿人类的操作
time.sleep(random.randint(2, 5))

infobook_page = "https://www.kanman.com/api/getuserinfobook?product_id=1&productname=kmh&platformname=pc&page=1&user_id=260809114&refresh=true&_=1696761852430"

# 发送请求，带上cookie，接受响应
res = requests.get(infobook_page, headers=headers, cookies=cookies)
json_data = res.json()

for comic_info in json_data["data"]["book_list"][0]["comic_info"]:
    print(comic_info["comic_name"])
```

> 方案二：代码模拟账户密码登录，自动获取cookie信息
>
> - 优点：爬虫实现自动化登录，解放双手
> - 缺点：每次请求需要回传上次请求响应的cookie，稍显繁琐

**方案三：使用Session，启动会话保持**

#### session

##### session简介

- **Session**中文翻译”会话“，可以理解为浏览器打开到关闭的过程
- 登陆期间，每次都要向服务器回传**cookie**，无形增加编码的复杂度，而Session正解决了这个问题
- **requests.Session**能让使用者跨请求保持某些参数如**cookie**，而且能自动处理服务器发来的**cookie**，使得同一个会话中的请求都带上最新的cookie，非常适合模拟登录

##### session使用

- `session = requests.Session()`
- 使用它发送的请求返回的cookie都会被它自动收集管理；每次发送新的请求，都会带上最新的cookie

```python
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
```

> 方案三：使用session开启会话，实现cookie收发自由
>
> - 优点：多个请求可以持续共享cookie信息
> - 缺点：无hhh

### 总结

![image-20231009081335905](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231009081335905.png)



# Multithread

### 线程用法

#### start

```python
import time


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


cook("1号厨师")
```

三个步骤依次进行，代码如上

```python
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

# 多线程任务
t1 = threading.Thread(target=cook, args=("1号厨师",))
t2 = threading.Thread(target=cook, args=("2号厨师",))
t3 = threading.Thread(target=cook, args=("3号厨师",))
t1.start()
t2.start()
t3.start()
```

#### join

当在最后一步加上`print("开始吃饭！")`会发现并不是在最后一步打印出来，因为此时有4个独立的线程都**并行**在计算机中执行

```python
t1 = threading.Thread(target=cook, args=("1号厨师",))
t2 = threading.Thread(target=cook, args=("2号厨师",))
t3 = threading.Thread(target=cook, args=("3号厨师",))
t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("开始吃饭！")
```

通过`start()`启动三个线程之后，调用`join()`分别等待三个线程的结束

请注意`t1.join()`被调用之后，如果t1线程没有结束，会停在方法调用处，等到t1线程执行结束了，流程才能进到下一步`t2.join()`

**目的：**<u>提高爬虫的爬取效率</u>

### 多线程爬取

```python
import requests
import time

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

for url in urls:
    res = requests.get(url, )
    print("访问{}结果：{}".format(url, res.status_code))

end = time.time()
print("共耗时：", end-start)
```

`共耗时： 1.4775028228759766`

```python
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
```

`共耗时： 0.9690432548522949`

从最后打印的时间可以看出，爬取的总耗时变短了。

### 总结

![image-20231009101133923](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231009101133923.png)



# Queue

#### 单线程方式

```python
import requests
import re

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
for i in range(len(data)):
    picture = requests.get(data[i]["verticalPic"])

    # 替换特殊字符 =====
    invalid_chars = re.compile(r'[\\/:"*?<>|]')
    name = invalid_chars.sub('_', data[i]["name"])

    with open("./tmp/pics/" + name + ".png", "wb") as file:
        file.write(picture.content)

# 共耗时： 3.8923592567443848
```

#### 多线程方式

先使用3个线程并行的方式进行图片请求和存储到磁盘的操作

```python
import requests
import re
import threading
import time

start = time.time()

def download_movie(number):
    for index in range(number*num_per_group, (number+1)*num_per_group):
        if index < pics_num:
            picture = requests.get(data[index]["verticalPic"])
            # 替换特殊字符
            invalid_chars = re.compile(r'[\\/:"*?<>|]')
            name = invalid_chars.sub('_', data[i]["name"])
            # 存入数据
            with open("./tmp/pics/" + name + ".png", "wb") as file:
                file.write(picture.content)


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
# 线程数量
thread_num = 3
# 每个线程最多处理多少个图片
num_per_group = pics_num // thread_num + 1

# 创建线程数组
threads = []
for i in range(thread_num):
    thread = threading.Thread(target=download_movie, args=(i,))
    thread.start()
    threads.append(thread)

# 等到所有线程结束
for thread in threads:
    thread.join()

end = time.time()
print("共耗时：", end-start)
# 共耗时： 2.5232858657836914
```

### 队列

> 单独的多线程问题

- 由于每个爬虫线程处理属于自己的独立集合的连接，在对某个信息进行爬取的时候，如果由于网络等问题导致爬取不流畅，还是会对效率造成影响
- 如果其他线程都完成了，但是一直卡在某一个线程中

> 于是我们采用队列的方式

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231009111954364.png" alt="image-20231009111954364" style="zoom:50%;" />

这样，即使某个线程在处理某个消息卡住时候，也不影响其他消息的处理过程

#### 队列的基本使用

```python
import threading
import queue

q = queue.Queue()

# 向队列中放入消息
for item in range(30):
    q.put(item)
print("所有消息放入完毕\n", end='')


# 使用线程去除队列中的消息
def worker():
    while q.qsize() > 0:
        item = q.get()
        print(f"处理消息: {item}")


# 创建5个线程
threads = []
for i in range(3):
    t = threading.Thread(target=worker)
    threads.append(t)

# 启动所有线程
for t in threads:
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

print("所有消息处理完毕")
```

#### 使用队列抓取图片

```python
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

end = time.time()
print("共耗时：", end - start)
# 共耗时： 1.3702361583709717
```

### 总结

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231009170015813.png" alt="image-20231009170015813" style="zoom:67%;" />



# DFS

### 爬取策略

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231010141920443.png" alt="image-20231010141920443" style="zoom:50%;" />

一个页面中一般有很多**a标签**，通过它们把多个页面相互连接起来

#### sitemap

可以通过它知道网站中的页面结构，快速的获取爬取的入口，甚至有时能直接得到要爬取的页面列表。

比如水木社区的https://www.mysmth.net/robots.txt 中，可以查到sitemap的地址

```txt
User-agent: Googlebot
Sitemap: https://www.newsmth.net/sitemap.xml
Allow: /index.html
Allow: /indexpages/
Allow: /frames.html
Allow: /mainpage.html
Allow: /bbsguestleft.html
Allow: /bbs0an.php
Allow: /bbsanc.php
Allow: /bbstcon.php
Allow: /sitemap.html
Allow: /sitemap.xml
```

打开`Sitemap`链接，可以看到如下内容

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231010142503534.png" alt="image-20231010142503534" style="zoom:50%;" />

这个网站的地图为我们列出了网站最关键的网页。主要内容被划分到10个分区中，它们的地址是 `http://www.mysmth.net/nForum/section/数字` 

- 要根据实际抓取情况，选择不同的方式。<u>可能还会使用广度优先与深度优先相结合得抓取方案</u>

#### 深度优先

```python
import requests
from bs4 import BeautifulSoup


def get_board_list(url, depth=1):
    headers = {
        'Referer': 'https://www.newsmth.net/nForum/',
        'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=21229206; main[UTMPNUM]=8449; Hm_lvt_3663c777a66d280fdb290b6b9808aff0=1696842267,1696919373; main[XWJOKE]=hoho; Hm_lpvt_3663c777a66d280fdb290b6b9808aff0=1696919542',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }

    res = requests.get(url, headers=headers)
    res.encoding = "GBK"

    soup = BeautifulSoup(res.text, 'lxml')
    board_table = soup.select_one(".board-list > tbody")
    title_1s = board_table.select(".title_1 > a")
    title_2s = board_table.select(".title_2")

    for i in range(len(title_1s)):
        board_name = title_1s[i].text
        board_author = title_2s[i].getText()
        abs_address = "https://www.mysmth.net"
        board_url = abs_address + title_1s[i].get("href")

        if board_author == "[二级目录]":
            print("xxxxxx子目录开始  ", board_name)

            if depth < 2:
                get_board_list(board_url, depth+1)
            else:
                print("爬取过深，跳过！")

            print("xxxxxx子目录结束  ", board_name)
        else:
            print("版面名称：", board_name)
            print('版面链接：', board_url)
            print('版主：', board_author)


url = 'https://www.newsmth.net/nForum/section/'
for i in range(10):
    print(f"===== 正在爬取Section{i} =====")
    get_board_list(url+str(i))

# 共耗时： 10.777654647827148
```

- 尤其注意用`depth`来控制深度
- DFS操作也被称为**递归**调用

#### 广度优先

```python
import requests
import bs4
import queue

def get_board_list(url):
    headers = {
        'Referer': 'https://www.newsmth.net/nForum/',
        'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=21229206; main[UTMPNUM]=8449; Hm_lvt_3663c777a66d280fdb290b6b9808aff0=1696842267,1696919373; main[XWJOKE]=hoho; Hm_lpvt_3663c777a66d280fdb290b6b9808aff0=1696919542',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }

    res = requests.get(url, headers=headers)
    res.encoding = "GBK"

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    board_table = soup.select_one(".board-list > tbody")
    title_1s = board_table.select(".title_1 > a")
    title_2s = board_table.select(".title_2")

    for i in range(len(title_1s)):
        board_name = title_1s[i].text
        board_author = title_2s[i].getText()
        abs_address = "https://www.mysmth.net"
        board_url = abs_address + title_1s[i].get("href")

        if board_author == "[二级目录]":
            q.put(board_url)
        else:
            print("版面名称：", board_name)
            print('版面链接：', board_url)
            print('版主：', board_author)


q = queue.Queue()

base_url = 'https://www.newsmth.net/nForum/section/'
for i in range(10):
    url = base_url + str(i)
    q.put(url)

    while not q.empty():
        url = q.get()
        get_board_list(url)
        
# 共耗时： 13.4683358669281
```

广度优先可以保证离开节点近得页面优先被访问，但如果某些网站的深度比较大，页面也很多，可能最底层得页面由于抓取规模得限制就得不到访问了。

#### 节奏控制

之前提过，为了不对服务器造成不必要的压力，也为了让爬虫能顺利得多爬回一些信息，在爬取不同页面的时候，需要添加一些等待时间，控制网站爬取的节奏。

- 在调用函数时，为了控制节奏，调用`time.sleep(random.randint(1,4))`让逻辑先等一等
- 等待时间使用随机数方式定义，而不是某个固定的值，看起来更像自然的网页访问

> 在该例子中，会发现DFS比BFS时间效率上会更快一点，所以我们结合两者优势

```python
import requests
import bs4
import queue
import time
import random


def get_board_list(url, isSection):
    # 随机等待抓取
    # time.sleep(random.randint(1,4))

    headers = {
        'Referer': 'https://www.newsmth.net/nForum/',
        'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=21229206; main[UTMPNUM]=8449; Hm_lvt_3663c777a66d280fdb290b6b9808aff0=1696842267,1696919373; main[XWJOKE]=hoho; Hm_lpvt_3663c777a66d280fdb290b6b9808aff0=1696919542',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
    }

    res = requests.get(url, headers=headers)
    res.encoding = "GBK"

    soup = bs4.BeautifulSoup(res.text, 'lxml')
    board_table = soup.select_one(".board-list > tbody")
    title_1s = board_table.select(".title_1 > a")
    title_2s = board_table.select(".title_2")

    for i in range(len(title_1s)):
        board_name = title_1s[i].text
        board_author = title_2s[i].getText()
        abs_address = "https://www.mysmth.net"
        board_url = abs_address + title_1s[i].get("href")

        if board_author == "[二级目录]":
            if isSection:
                q.put(board_url)
            else:
                get_board_list(board_url, isSection)
        else:
            print("版面名称：", board_name)
            print('版面链接：', board_url)
            print('版主：', board_author)


q = queue.Queue()

base_url = 'https://www.newsmth.net/nForum/section/'
for i in range(10):
    url = base_url + str(i)
    q.put(url)

    while not q.empty():
        url = q.get()
        get_board_list(url, isSection=True)

        while not q.empty():
            url = q.get()
            get_board_list(url, isSection=False)
```

虽然在这个例子中，爬取时间没有减少，但是这样的逻辑更符合在大量爬取信息中的逻辑。先优先爬取最上层的BFS，然后对于下层的再进行DFS爬取。

### 总结

- 我们了解了网站的sitemap，可以通过它知道网站中的页面结构，快速的获取爬取的入口，甚至有时能直接得到要爬取的页面列表。

- 对于页面的爬取，可以使用深度优先的爬取策略，它沿着最先看到的分支可以一直深入地爬取，将藏得很深的页面也能爬取出来。但在爬取大量页面时，有可能由于爬取量太大，会使得某些浅层的页面没被爬取。

- 也可以使用广度优先的策略进行爬取，它对距离开始节点最近的页面做优先爬取，大部分场景中能最大可能地实现首先爬取重要网页的功能。但层次比较深的页面却有可能因为爬取数量限制导致被遗漏。

- 在实际应用过程中，深度优先和广度优先的策略可以结合使用，同时我们需要注意控制爬取的速率，防止对服务器造成不应有的过高压力。

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231011224417870.png" alt="image-20231011224417870" style="zoom:80%;" />



# Scrapy框架

**Scrapy**是一个为爬取网站数据、提取结构性数据而编写的应用框架，该框架是纯Python实现的，也是目前Python中最受欢迎的爬虫框架之一。

### scrapy框架构成

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231004101810833.png" alt="image-20231004101810833" style="zoom:80%;" />**Scrapy Engine**：是整个框架的引擎，主要负责Spider、ItemPipeline、Downloader、Scheduler各组件之间的通讯，完成信号及数据的传递等。

**Scheduler**：是调度器，它负责接收所有**请求url**，对其进行**去重、排列、入队**。

**Downloader**：是下载器，它负责去网络中**下载网页信息**，完成网络资源的下载。

**Spider**：是爬虫，它负责处理所有**Responses**，从中分析提取数据，并提供初始爬取的url。

**ItemPipeline**：是数据管道，它负责接收Item数据，并进行后期处理如**数据分析、清洗、入库**等。

**Downloader Middlewares**：翻译过来是下载中间件，你可以理解为下载器的小助理。

**Spider Middlewares**：翻译过来是爬虫中间件，你可以理解为爬虫的小助理。



### scrapy框架原理

- Step1：**Spider**中提供**初始url**交给引擎，引擎交给调度器入队。

- Step2：引擎从调度器获取请求url交给下载器。

- Step3：下载器接收引擎传递的请求，完成从互联网下载页面，生成response对象返回给引擎。

- Step4：引擎将response交给爬虫。

- Step5：爬虫接收引擎传递来的response，并从中解析出数据返回给引擎（其中一部分是目标数据会打包暂存在item中，另一部分是需要跟进的url）。

- Step6：引擎将返回数据中的item交给数据管道，将需要再次跟进的URL交给调度器，进入请求队列。

- Step7：管道接收引擎传递来的item，对其进行清洗、验证、去重、入库等操作。

如果**请求队列为空**则结束爬取任务，否则一直重复Step2~Step7的工作。

![image-20231004102356124](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231004102356124.png)



### scrapy框架使用

1. 创建项目之前，需要先安装环境，打开你的终端输入安装指令：`conda install scrapy`
2. 进入终端（cmd）
3. 使用`cd命令`进入你要创建项目的目录
4. 输入创建scrapy项目的命令：`scrapy startproject 项目名称`。点击Enter键。



点开项目目录，内部是一个与项目同名的文件夹，还有一个scrapy的配置文件

![image-20231004104712273](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231004104712273.png)



![image-20231004104659447](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231004104659447.png)

简单介绍一下它们各自的作用：

1. **spiders**目录存放你编写的**爬虫代码文件**。

2. **init.py**文件存放一些项目启动的**初始化信息**。

3. **items.py**文件是保存抓取数据的容器，其存储方式类似于Python的字典。

4. **middlewares.py**文件中可以定制你需要的中间件。

5. **piplines.py**文件中编写数据的存储逻辑，定制数据的存储格式。

6. **settings.py**文件中是项目的设置信息，例如统一设置请求头、是否遵循君子协议等。

其中的文件**<u>不可以</u>**擅自修改名称，只能按照一定的模范在其中添加你的代码



### 网页分析

> 爬取中国高校2020年度的排行榜：http://www.cnur.com/rankings/188.html

#### 创建项目文件

- 打开终端，进入spiders文件夹，然后输入：`scrapy genspider 文件名 url` 
  - (e.g. `scrapy genspider first http://www.cnur.com`)

**FirstSpider**类中又三分属性和一个方法，介绍如下：

- **name**是**爬虫名**，后续启动爬虫需要用到
- **allowed_domains**是爬取的**域名**, **start_urls**是爬取的**初始url**
  - allowed_domains和start_urls的数据是**列表**，意味着可以添加多个域名或url
  - <u>自动生成的url可以进行修改</u>
- **parse**方法是**默认解析方法**

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231012090002265.png" alt="image-20231012090002265" style="zoom:67%;" />



#### 编写代码

接下来要在parse中编写解析响应页面、提取目标数据的代码

```python
# first.py

import scrapy
from bs4 import BeautifulSoup


class FirstSpider(scrapy.Spider):
    name = "first"
    allowed_domains = ["www.cnur.com"]
    start_urls = ["http://www.cnur.com/rankings/188.html"]

    def parse(self, response):

        # 解析响应，抽取目标数据
        soup = BeautifulSoup(response.text, "lxml")
        # 去掉表头的数据
        tags = soup.find_all("tr", style=";height:30px")[1:]
        # 打印榜单排名信息
        for tag in tags:
            info = list(tag.strings)
            print("2020年度中国搞笑排名第{}的是{}".format(info[0], info[1]))
        
        pass
```

- 我们使用`find_all`方法，获取所有`tr标签`的列表，然后通过列表切片`[1:]`过滤掉不需要的**表头数据标签**。

- 接着，遍历`tags`列表中的`tr标签`，通过`tag.strings`获取每一个`tr标签`下所有子标签(`td`)的文本内容。

- 需要注意的是`tag.strings`返回的是生成器(`generator`)，你可以理解为返回内容被打包装在一起。

- 解开包装的方法是：`list(tag.strings)`。

#### 添加设置

> 在运行前我们需要在`setting.py`文件中完成一部分设置，否则...爬了个寂寞

1. 找到变量`ROBOTSTXT_OBEY`并将默认值修改为`False`，代表不遵循君子协议。遵照协议大部分有价值的信息我们都爬不到。
2. 设置默认的请求头，在`DEFAULT_REQUEST_HEADERS`字典中添加`User-Agent`信息，模拟浏览器。
3. 设置程序日志的输出等级，变量`LOG_LEVEL`的值设置为`'ERROR'`。在进行日志打印时，只打印`ERROR`级别的日志。

#### 运行爬虫

1. 打开终端，输入`scrapy crawl 爬虫名`

> ../../../testPorject/testProject> scrapy crawl first

2. 新建一个文件，添加如下代码，然后Run

```python
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'first'])
```

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231012095139709.png" alt="image-20231012095139709" style="zoom: 67%;" />



### 总结

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231012095716676.png" alt="image-20231012095716676" style="zoom:67%;" />



# Scrapy框架应用

### 任务发布

今天我们的任务是，爬取前程无忧网站上发布的python职位信息，保存到本地。

目标站点：[https://www.51job.com](https://www.51job.com/)

我们的目标数据是，拿到每一个招聘职位的详细信息包括**公司名称、职位名称、薪资、工作地址、公司主页链接**。

### scrapy框架使用流程

上一节的案例不涉及数据存储，我们增加这一流程

<img src="C:\Users\65324\Desktop\小象学院\interactive_course\spider\chapter3\3_scrapy_example_files\89280eb57e2d15276d59a3ac11bbb2cb.gif" alt="89280eb57e2d15276d59a3ac11bbb2cb" style="zoom:50%;" />

存储数据的逻辑，我们需要在items.py和pipelines.py文件中编写相应的代码。

#### ItemPipelines组件

##### items.py

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231012102212672.png" alt="image-20231012102212672" style="zoom: 67%;" />

```python
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestprojectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    age = scrapy.Field()
    score = scrapy.Field()
    pass


t = TestprojectItem()

t['name'] = '小象'
t['age'] = 39
t['score'] = 98

print(t)
print(t['name'])
print(t['age'])
print(t['score'])
```

- 在python中字典、列表、元组等都是存放数据的容器
- `TestproItem`类创建的对象也是同样的功能，是scrapy框架中存放数据的容器。

**结论**：scrapy.Item的继承类(也就是本例中的`TestprojectItem`)可以创建类似Python字典的容器对象，用于存储爬取的数据。

- `scrapy.Field()`你可以理解为字典的`“Key”`，后期爬取的数据就是`“Value“`。

- 在使用scrapy框架时，一般我们会先确定目标数据，在items.py文件中定义字典的`“Key”`。

我需要提醒你的是，<u>items只是**暂存数据的容器**</u>。

如果你想将数据永久保存，例如文件形式保存到本地(Csv、Execl)或者远程数据库(Mysql)，还需要items的好兄弟pipelines来帮忙。

##### pipline.py

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231012102656404.png" alt="image-20231012102656404" style="zoom: 67%;" />

pipeline.py文件中为你提供了代码模板，你的持久化存储数据的代码需要在这个预置的类中自己实现。



### 代码实现

#### 创建爬虫项目

使用`scrapy startproject 项目名`命令创建项目，你可以顺带在spiders目录下使用`scrapy genspider 文件名 [域名]`命令，新建一个爬虫文件。

#### 定义数据容器

在items.py文件中定义数据容器，明确爬取的目标数据，参考代码如下。

```python
class TestproItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()  # 公司名称
    job_name = scrapy.Field()  # 职位名称
    salary = scrapy.Field()  # 薪资
    address = scrapy.Field()  # 地址
    company_url = scrapy.Field()  # 公司主页网址
    
    pass
```

#### 编写爬取逻辑

在spider目录下的文件中完成爬取逻辑编写，参考代码如下

```python
import scrapy
import json
from bs4 import BeautifulSoup
from testpro.items import TestproItem

class WyJobSpider(scrapy.Spider):
    # 定义爬虫名
    name = '51job'
    allowed_domains = ['search.51job.com', 'jobs.51job.com']
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    
    def start_requests(self):
        for pg in range(1,2):
            url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,{pg}.html?' \
                  'lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99' \
                  '&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(pg=pg)
            yield scrapy.Request(url=url, headers = self.header, callback=self.parse)
            
            
    # 接收列表页响应，解析出每个职位的职位信息，构建item并返回给引擎
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # 利用有id属性的div标签，定位与之相邻的script标签，获取标签文本
        data_text = soup.find('div', {'id': 'app'}).find_next('script', {'type': 'text/javascript'}).string.split('=',1)[1]
        # 将json格式转换成python的字典类型
        data_dict = json.loads(data_text)
        # 获取职位信息列表
        job_list = data_dict["engine_search_result"]
        
        # 遍历职位列表，获取每个职位的信息并生成Item，返回给引擎
        for job in job_list:
            company = job['company_name']
            company_url = job['company_href']
            job_name = job['job_name']
            salary = job['providesalary_text']
            address = job['workarea_text']
            print(company)
            print(company_url)
            print(job_name)
            print(salary)
            print(address)
            print('=' * 100)
            
            item = TestproItem()
            item['company'] = company
            item['company_url'] = company_url
            item['job_name'] = job_name
            item['salary'] = salary
            item['address'] = address
            yield item
```

（不过该代码与现实爬取时候的网页分析不一致，仅了解思路即可，此代码无法运行）



#### 编写存储逻辑

在pipelines.py文件中编写将爬取的数据持久化保存到本地的代码，以csv文件为列参考代码如下：

```python
from itemadapter import ItemAdapter

import csv

class TestproPipeline:
    # 爬虫启动时执行一次的方法
    def open_spider(self, spider):
        self.headers = ["company", "job_name", "salary", "address", "company_url"]
        # 打开csv文件添加表头
        with open("../../tmp/C_data.csv", "a+") as f:
            self.f_csv = csv.writer(f)
            self.f_csv.writerow(self.headers)

    # 默认处理数据的方法
    def process_item(self, item, spider):
        # 从Item中取出数据，写入csv文件
        rows = [item["company"], item["job_name"], item["salary"], item["address"], item["company_url"]]
        with open("../../tmp/C_data.csv", "a+") as f:
            self.f_csv = csv.writer(f)
            self.f_csv.writerow(rows)
            
        return item
```

- 使用`with open`语句打开文件时，要选择追加模式`a+`，能够**避免数据被覆盖**

- `TestproPipeline`类中实现了两个方法`open_spider`和`process_item`。
  - `open_spider`只在爬虫启动时执行一次，我们利用这个特征，在其中实现添加表头的代码。
  - `process_item`是默认的存储数据的方法，每次引擎接收爬虫中获取的数据Item，就会调用该方法对Item进行后续的处理，我们在这个方法中实现追加数据的代码。



#### 修改设置内容

- 在setting.py文件中添加相应的设置

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231019180343654.png" alt="image-20231019180343654" style="zoom: 80%;" />



- 这次涉及到数据存储

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231019180430133.png" alt="image-20231019180430133" style="zoom:67%;" />



#### 运行爬虫项目

1. `scrapy crawl 51job` 命令运行项目

2. 新建`run.py`文件，然后运行

   ```python
   from scrapy import cmdline
   
   if __name__ == '__main__':
       cmdline.execute(['scrapy', 'crawl', '51job'])
   ```



### 总结

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231019180936385.png" alt="image-20231019180936385" style="zoom:80%;" />

# Crawl Weibo

### 抓取单页

抓取微博评论

```python
import requests

url = "https://m.weibo.cn/comments/hotflow"

query_string = {
    "id": "4564698990907350",
    "mid": "4564698990907350",
    "max_id_type": "0",
}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Mweibo-Pwa": "1",
    "Referer": "https://m.weibo.cn/detail/4564698990907350",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
    "X-Requested-With": "XMLHttpRequest",
    "X-Xsrf-Token": "4bc924",
}

res = requests.get(url, headers=headers, params=query_string)

comments = res.json()

for item in comments["data"]["data"]:
    print("========")
    print("用户：", item["user"]["screen_name"])
    print("评论：", item["text"])
```

用户： 帅宝妈咪2011
评论： 大美璇儿<span class="url-icon"><img alt=[爱你] src="https://h5.sinaimg.cn/m/emoticon/icon/default/d_aini-09d5f3f870.png" style="width:1em; height:1em;" /></span>

（但是会发现有除文字之外的内容出现，HTML格式）

改为如下

```python
# print("评论：", item["text"])

soup = bs4.BeautifulSoup(item["text"], "lxml")
print("评论：", soup.text)
```

### 登录抓取更多评论

在向下不停滚动的时候，加载出更多的评论页面，会出现账号登录提示。

这时候需要用Selenium来管理这个操作流程。

1. 先单独获取一页内容：

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

browser_options = Options()
browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
time.sleep(2)

browser.get("https://m.weibo.cn/detail/4564698990907350")
time.sleep(5)

# 提取评论用户名和内容
comment_content = browser.find_element_by_class_name("comment-content")
user_names = comment_content.find_elements_by_tag_name("h4")
comments = comment_content.find_elements_by_tag_name("h3")

for i in range(len(comments)):
    print("======")
    print("用户：", user_names[i].text)
    print("评论：", comments[i].text)

browser.quit()
```



2. 爬取多页内容（配合人机交互）

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

# 1. 打开页面
browser = webdriver.Firefox(executable_path='data/geckodriver.exe')
time.sleep(2)
browser.get('https://m.weibo.cn/detail/4564698990907350')

# 2.1 等待验证码页面出现
while True:
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.verify-box'))
        )
        break
    except TimeoutException:
        print('未登录，继续等待。')

# 2.2 等待登录成功
while True:
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'comment-content'))
        )
        break
    except TimeoutException:
        print('未登录成功，继续等待。')

# 3. 滚动三页，输出评论内容
for i in range(3):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3)

comment_content = browser.find_element_by_class_name('comment-content')
user_names = comment_content.find_elements_by_tag_name('h4')
comments = comment_content.find_elements_by_tag_name('h3')

for i in range(len(comments)):
    print('======')
    print('用户：', user_names[i].text)
    print('评论：', comments[i].text)

browser.quit()
```

- 在2.1和2.2一直等待人工登录操作
- 使用selenium中的**WebDriverWait**和**expected_conditions**配合实现**让程序等待**的功能
  - 例子中的`until()`里，使用`expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.verify-box'))`定义的事件是**登录验证窗口在页面中出现**。
  - 这里参数中的`By.CSS_SELECTOR`表示我们希望通过CSS选择器定位元素，`'.verify-box'`这个CSS选择器就表示了要定位元素的class是**verify-box**。
  - 这次等待的事件是`expected_conditions.presence_of_element_located((By.CLASS_NAME, 'comment-content'))`，帖子的评论区重新显示在网页上。如果评论区重新出现，就表示登录操作完成了。
  - 这里有意使用了跟2.1不太一样的方法作为例子，其实使用CSS选择器也可以达到相同的目的，即：`expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.comment-content'))`。



3. 保存到文件

```python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import openpyxl

browser = webdriver.Firefox(executable_path = "data/geckodriver.exe")
time.sleep(2)
browser.get("https://m.weibo.cn/detail/4564698990907350")

# 等到验证码页面出现
while True:
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".verify-box"))
        )
        break
    except TimeoutException:
        print("未登录，继续等待。")

# 等待登录成功
while True:
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, "comment-content"))
        )
        break
    except TimeoutException:
        print("未登录成功，继续等待。")


# 滚动三页
for i in range(3):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight")
    time.sleep(3)

# 输出和存储评论内容
comment_content = browser.find_elements_by_class_name("comment-content")
user_names = comment_content.find_elements_by_name("h4")
comments = comment_content.find_elements_by_tag_name("h3")

# 新建工作簿、指定第一行标题
wb = openpyxl.Workbook()
sheet = wb.active
sheet['A1'] = '用户名'
sheet['B1'] = '评论'

# 在循环输出内容的同时，通过sheet.append()方法添加每行内容
for i in range(len(comments)):
    print("======")
    print("用户：", user_names[i].text)
    print("评论：", comments[i].text)
    sheet.append({'A': user_names[i].text, 'B': comments[i].text})

wb.save("./tmp/评论.xlsx")
browser.quit()
```

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231023000026404.png" alt="image-20231023000026404" style="zoom:50%;" />

<u>（该代码无法完整运行***，验证失败）</u>



### 总结

<img src="C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231023000101971.png" alt="image-20231023000101971" style="zoom:67%;" />