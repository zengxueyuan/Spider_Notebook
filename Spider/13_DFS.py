# import requests
# from bs4 import BeautifulSoup
# import time
#
#
# def get_board_list(url, depth=1):
#     headers = {
#         'Referer': 'https://www.newsmth.net/nForum/',
#         'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=21229206; main[UTMPNUM]=8449; Hm_lvt_3663c777a66d280fdb290b6b9808aff0=1696842267,1696919373; main[XWJOKE]=hoho; Hm_lpvt_3663c777a66d280fdb290b6b9808aff0=1696919542',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
#     }
#
#     res = requests.get(url, headers=headers)
#     res.encoding = "GBK"
#
#     soup = BeautifulSoup(res.text, 'lxml')
#     board_table = soup.select_one(".board-list > tbody")
#     title_1s = board_table.select(".title_1 > a")
#     title_2s = board_table.select(".title_2")
#
#     for i in range(len(title_1s)):
#         board_name = title_1s[i].text
#         board_author = title_2s[i].getText()
#         abs_address = "https://www.mysmth.net"
#         board_url = abs_address + title_1s[i].get("href")
#
#         if board_author == "[二级目录]":
#             print("xxxxxx子目录开始  ", board_name)
#
#             if depth < 2:
#                 get_board_list(board_url, depth+1)
#             else:
#                 print("爬取过深，跳过！")
#
#             print("xxxxxx子目录结束  ", board_name)
#         else:
#             print("版面名称：", board_name)
#             print('版面链接：', board_url)
#             print('版主：', board_author)
#
#
# start = time.time()
# url = 'https://www.newsmth.net/nForum/section/'
# for i in range(10):
#     print(f"===== 正在爬取Section{i} =====")
#     get_board_list(url+str(i))
# end = time.time()
# print("共耗时：", end - start)



# import requests
# import bs4
# import queue
# import time
#
# def get_board_list(url):
#     headers = {
#         'Referer': 'https://www.newsmth.net/nForum/',
#         'Cookie': 'main[UTMPUSERID]=guest; main[UTMPKEY]=21229206; main[UTMPNUM]=8449; Hm_lvt_3663c777a66d280fdb290b6b9808aff0=1696842267,1696919373; main[XWJOKE]=hoho; Hm_lpvt_3663c777a66d280fdb290b6b9808aff0=1696919542',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
#     }
#
#     res = requests.get(url, headers=headers)
#     res.encoding = "GBK"
#
#     soup = bs4.BeautifulSoup(res.text, 'lxml')
#     board_table = soup.select_one(".board-list > tbody")
#     title_1s = board_table.select(".title_1 > a")
#     title_2s = board_table.select(".title_2")
#
#     for i in range(len(title_1s)):
#         board_name = title_1s[i].text
#         board_author = title_2s[i].getText()
#         abs_address = "https://www.mysmth.net"
#         board_url = abs_address + title_1s[i].get("href")
#
#         if board_author == "[二级目录]":
#             q.put(board_url)
#         else:
#             print("版面名称：", board_name)
#             print('版面链接：', board_url)
#             print('版主：', board_author)
#
#
# start = time.time()
# q = queue.Queue()
#
# base_url = 'https://www.newsmth.net/nForum/section/'
# for i in range(10):
#     url = base_url + str(i)
#     q.put(url)
#
#     while not q.empty():
#         url = q.get()
#         get_board_list(url)
#
# end = time.time()
# print("共耗时：", end - start)




############################
## 相结合 #############
###########################

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


start = time.time()
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

end = time.time()
print("共耗时：", end - start)
