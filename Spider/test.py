import json
import re
import requests


url = "https://www.bilibili.com/video/BV1rg4y1L7Aa/?spm_id_from=333.337.search-card.all.click&vd_source=d27fa28962a6946266e8c93b1c5d9c5c"
headers = {
    "Referer": "https://search.bilibili.com/all?keyword=%E4%B8%8D%E4%B8%BA%E8%B0%81%E8%80%8C%E4%BD%9C%E7%9A%84%E6%AD%8C+mv&from_source=webtop_search&spm_id_from=666.25&search_source=2",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46",
}

res = requests.get(url=url, headers=headers).text
txt_a = re.findall(r"<script>window.__playinfo__=(.*?)</script>", res, re.S)[0]
txt_json = json.loads(txt_a)
audio_url = txt_json['data']['dash']['audio'][0]['baseUrl']
video_url = txt_json['data']['dash']['video'][0]['baseUrl']

audio_txt = requests.get(url=audio_url, headers=headers).content
video_txt = requests.get(url=video_url, headers=headers).content
with open("./不为谁而作的歌_bilibili.mp3", mode="wb") as f:
    f.write(audio_txt)
with open("./不为谁而作的歌_bilibili.mp4", mode="wb") as f:
    f.write(video_txt)
