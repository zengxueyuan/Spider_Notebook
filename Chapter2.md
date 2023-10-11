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

![image-20231009170015813](C:\Users\65324\AppData\Roaming\Typora\typora-user-images\image-20231009170015813.png)