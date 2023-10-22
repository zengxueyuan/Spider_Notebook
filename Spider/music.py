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
