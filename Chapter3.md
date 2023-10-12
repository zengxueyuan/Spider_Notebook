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

（但是会发现有除文字之外的内容出现，HTML格式

改为如下

```python
# print("评论：", item["text"])

soup = bs4.BeautifulSoup(item["text"], "lxml")
print("评论：", soup.text)
```

### 登录抓取更多评论



