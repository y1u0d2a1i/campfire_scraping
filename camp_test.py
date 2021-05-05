import requests
from bs4 import BeautifulSoup
import re
import csv
import math

def get_info(box,class_selector,default_text):
    info_box = box.select(f'div.overview > div.{class_selector}')
    if info_box:
        before_info = info_box[0].get_text()
        # 数字のみにする
        info = re.sub(r"\D", "", before_info)
    else:
        info = default_text

    return info

all_data_list = []

target_url = f"https://camp-fire.jp/projects/search?page=4&word=プロテイン"
r = requests.get(target_url)
soup = BeautifulSoup(r.text, 'lxml')

# all_boxes = soup.find('div',{'class':'box'})
all_boxes = soup.select('body > div.projects-search.layouts-projects.projects-search.wrapper > div > section > div > div.sp-box-outer > div.boxes4.clearfix > div')

# スクレイピングで情報取得
for box in all_boxes:
    a = box.select('div.box-title a')[-1]
    print(a)
    if a:
        title = a.select('h4')[0].get_text()
        link = a['href']
    else:
        continue
    print(title)

    total = get_info(box,'total','0円')
    supporter = get_info(box,'rest','0人')
    day = get_info(box,'per','0日')

    # 詳細ページへ
    detail_url = f'https://camp-fire.jp{link}'
    detail_r = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_r.text, 'lxml')

    target_price_box = detail_soup.select('div.project_status > div > span')
    if target_price_box:
        before_target_price = target_price_box[0].get_text()
        target_price = re.sub(r"\D", "", before_target_price)
    else:
        target_price = "情報なし"

    message_box = detail_soup.select('section.caption.sp-none > h2')
    if message_box:
        message = message_box[0].get_text()
    else:
        message = "説明なし"

    data_list = [title,supporter,day,total,target_price,message,detail_url]
    all_data_list.append(data_list)
    # print(title,link,total,supporter,day,target_price,message)

# with open('data.csv','a') as f:
#     writer = csv.writer(f)
#     writer.writerows(all_data_list)
