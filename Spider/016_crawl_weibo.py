# import requests
# import bs4
#
# url = "https://m.weibo.cn/comments/hotflow"
#
# query_string = {
#     "id": "4564698990907350",
#     "mid": "4564698990907350",
#     "max_id_type": "0",
# }
#
# headers = {
#     "Accept": "application/json, text/plain, */*",
#     "Mweibo-Pwa": "1",
#     "Referer": "https://m.weibo.cn/detail/4564698990907350",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "Windows",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
#     "X-Requested-With": "XMLHttpRequest",
#     "X-Xsrf-Token": "4bc924",
# }
#
# res = requests.get(url, headers=headers, params=query_string)
#
# comments = res.json()
#
# for item in comments["data"]["data"]:
#     print("========")
#     print("用户：", item["user"]["screen_name"])
#     # print("评论：", item["text"])
#     soup = bs4.BeautifulSoup(item["text"], "lxml")
#     print("评论：", soup.text)

# ==============================


# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
#
# # 1. 打开页面
# browser_options = Options()
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
# time.sleep(2)
#
# browser.get("https://m.weibo.cn/detail/4564698990907350")
# time.sleep(5)
#
# # 提取评论用户名和内容
# comment_content = browser.find_element_by_class_name("comment-content")
# user_names = comment_content.find_elements_by_tag_name("h4")
# comments = comment_content.find_elements_by_tag_name("h3")
#
# for i in range(len(comments)):
#     print("======")
#     print("用户：", user_names[i].text)
#     print("评论：", comments[i].text)
#
# browser.quit()


# ==========================


# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
# import time
#
# # 1. 打开页面
# browser = webdriver.Firefox(executable_path='data/geckodriver.exe')
# time.sleep(2)
# browser.get('https://m.weibo.cn/detail/4564698990907350')
#
# # 2.1 等待验证码页面出现
# while True:
#     try:
#         wait = WebDriverWait(browser, 10)
#         wait.until(
#             expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.verify-box'))
#         )
#         break
#     except TimeoutException:
#         print('未登录，继续等待。')
#
# # 2.2 等待登录成功
# while True:
#     try:
#         wait = WebDriverWait(browser, 10)
#         wait.until(
#             expected_conditions.presence_of_element_located((By.CLASS_NAME, 'comment-content'))
#         )
#         break
#     except TimeoutException:
#         print('未登录成功，继续等待。')
#
# # 3. 滚动三页，输出评论内容
# for i in range(3):
#     browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#     time.sleep(3)
#
# comment_content = browser.find_element_by_class_name('comment-content')
# user_names = comment_content.find_elements_by_tag_name('h4')
# comments = comment_content.find_elements_by_tag_name('h3')
#
# for i in range(len(comments)):
#     print('======')
#     print('用户：', user_names[i].text)
#     print('评论：', comments[i].text)
#
# browser.quit()


# ===========================

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
