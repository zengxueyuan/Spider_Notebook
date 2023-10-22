# from selenium import webdriver
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
# browser.get("https://www.suning.com/")
#

#
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
#
# browser_options = Options()
# browser_options.add_argument("--headless")
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe", options=browser_options)
# # 等待两秒，保证浏览器加载完成
# time.sleep(2)
#
# browser.get("https://www.suning.com/")
# # 获取HTML内容并打印
# html = browser.page_source
# print(html)
#
# # 保存页面截图
# browser.save_screenshot("tmp/screen_shot.png")

# browser.quit()
#
#


#
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# import time
#
# browser_options = Options()
# browser_options.add_argument("--headless")
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe", options=browser_options)
#
# # 等待两秒，保证浏览器加载完成
# time.sleep(2)
#
# browser.get("https://www.suning.com/")
#
# # 查找搜索框元素并输入关键字
# search_box = browser.find_element_by_css_selector("#searchKeywords")
# search_box.send_keys("手机")
#
# # 等待两秒，保证搜索结果加载完成
# time.sleep(2)
#
# # 获取HTML内容并打印
# html = browser.page_source
# print(html)
#
# # 保存页面截图
# browser.save_screenshot("tmp/screen_shot.png")
#
# browser.quit()


# from selenium import webdriver
# import time
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
# time.sleep(1)
#
# browser.get("https://www.suning.com/")
#
# # 查找搜索框元素并输入关键字
# search_box = browser.find_element_by_css_selector("#searchKeywords")
# search_box.send_keys("手机")
#
# # 查找搜索按钮元素并点击
# search_button = browser.find_element_by_css_selector("#searchSubmit")
# search_button.click()
#
# # 等待两秒，保证搜索结果加载完成
# time.sleep(2)
#
# browser.quit()

#
# from selenium import webdriver
# import time
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
# time.sleep(2)
#
# # 访问页面
# browser.get("https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html?safp=d488778a.homepagev8.126605238627.65&safc=cate.0.0&safpn=10001")
# # 获取页面快照
# ret = browser.save_screenshot("tmp/huawei.png")
# print("快照拍摄结果：", ret)
#
# browser.quit()

#
# from selenium import webdriver
# import time
# import bs4
#
# # ==== BeautifulSoup =====
# # def products_info():
# #     print("获取商品信息：")
# #     # 读取HTML页面
# #     html = browser.page_source
# #     # 加载页面内容
# #     soup = bs4.BeautifulSoup(html, "lxml")
# #     items = soup.select(".title-selling-point")
# #     # 遍历商品信息
# #     for item in items:
# #         print("======")
# #         title = item.text.strip()
# #         print(title)
#
# # ==== Selenium ====
# def products_info():
#     print("获取商品信息：")
#     items = browser.find_elements_by_class_name("title-selling-point")
#     for item in items:
#         print("=====")
#         print(item.text)
#
#
# browser = webdriver.Firefox(executable_path="data/geckodriver.exe")
# time.sleep(2)
#
# browser.get(
#     "https://list.suning.com/0-20006-0-0-0-0-0-0-0-0-11635.html?safp=d488778a.homepagev8.126605238627.65&safc=cate.0.0&safpn=10001")
#
# # 将页面滚动到底部
# browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#
# item_wraps = browser.find_elements_by_class_name('item-wrap')
#
# while len(item_wraps) < 120:
#     # 将页面滚动到底部
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#
#     item_wraps = browser.find_elements_by_class_name('item-wrap')
#     # print(len(item_wraps))
#
#     time.sleep(2)
#
# # 调用函数获取相关信息
# products_info()
#
# next_page_button = browser.find_element_by_id("nextPage")
# next_page_button.click()
# time.sleep(5)
#
# browser.quit()


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
        # print(len(item_wraps))

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

for i in range(3):
    get_page()
    time.sleep(2)

browser.quit()
