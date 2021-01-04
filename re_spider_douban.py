# 用正则抓取豆瓣网信息

import requests
import re
import os

url = "https://movie.douban.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"}
response = requests.get(url,headers = headers)
print(response.status_code)
html = response.text
# print(html)

ret = re.findall(r'"(http[s]?.*?\.(jpg|png|gif|bmp|webp))"', html)
print(ret) # 爬取的图片格式：('https://img3.doubanio.com/f/movie/caa8f80abecee1fc6f9d31924cef8dd9a24c7227/pics/movie/ic_new.png', 'png')

# 这里创建收集爬取的图片的文件夹
if not os.path.exists('imgs'):
    os.makedirs('imgs')

for id,pic_url in enumerate(ret):
    print(id,pic_url)
    # id：是编号  pic_url：(图片地址，图片格式)
    # 把图片存在本地 => 二进制文件 => content
    #                            => text => content转化成str
    img = requests.get(pic_url[0], headers=headers).content
    # filepath = output_dir/i.pic_url[1]
    filepath = "imgs/{}.{}".format(id,pic_url[1])
    print(filepath)
    with open(filepath, 'wb') as f:
        f.write(img)







