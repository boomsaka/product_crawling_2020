#!/usr/bin/env python
# coding: utf-8

import requests
from lxml import etree
import re
import json
import csv
import urllib3
from bs4 import BeautifulSoup
import time
urllib3.disable_warnings()

def create_csv(file_name):
    with open(file_name+".csv", "w", encoding="utf-8-sig", newline="") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(columns)

def save_data(data, file_name):
    with open(file_name+".csv", "a", encoding="utf-8-sig", newline="") as f:
        csv_f = csv.writer(f)
        csv_f.writerow([data.get(key) for key in columns])

def extract_data(resp, file_name):
    soup = BeautifulSoup(resp.text, "lxml")
    base = soup.find_all("div", class_="qMZa55 SQGpu8 iOzucJ JT3_zV DvypSJ")
    for each in base:
        extract_detail(each, file_name)
    print(soup.find("div", class_="cat_label-2W3Y8").text)
    page, pages = re.findall("\d+\.?\d*",soup.find("div", class_="cat_label-2W3Y8").text)
    return pages

def extract_all_data(ori_url, sup):
    resp = requests.get(ori_url, headers=headers, verify=False)
    if resp.ok:
        total_pages = extract_data(resp, sup)
    else:
        print('''The connection to the website failed, please check the url or anti-crawler.''')
    for p in range(2, int(total_pages)+1):
        time.sleep(3)
        url = ori_url+"?p={}".format(p)
        resp = requests.get(url, headers=headers, verify=False)
        if resp.ok:
            extract_data(resp, sup)

def extract_detail(each, file_name=False):
    brand = each.find("div", class_="_0xLoFW _78xIQ- EJ4MLB JT3_zV").find("div", class_="hPWzFB").find("span").text
    product = " - ".join(each.find("div", class_="_0xLoFW _78xIQ- EJ4MLB JT3_zV").find("div", class_="hPWzFB").find("h3").text.split(" - ")[:-1])
    prices = each.find("div", class_="_0xLoFW _78xIQ- EJ4MLB JT3_zV").find("div", class_="_0xLoFW u9KIT8 _7ckuOK").text.split(" ")
    if len(prices) > 2:
        ori_price = prices[-1].replace("\xa0","").replace(",",".")
        now_price = prices[-2].replace("\xa0","").replace(",",".")
    else:
        ori_price = now_price = prices[-1].replace("\xa0","").replace(",",".")
    img_link = each.find("img").get("src")
    product_link = "https://www.zalando.fr"+each.find("a").get("href")
    if file_name:
        save_data(dict(zip(columns, [brand, product, ori_price, now_price, img_link, product_link])), file_name)

def main(sup):
    url = "https://www.zalando.fr/"+sup
    global columns, headers
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
                      'ebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
    }
    columns = ["brand","product","original price","current price","image url","product url"]
    create_csv(sup)
    extract_all_data(url, sup)
    
for i in ["nuisettes-pyjamas-femme", "pyjamas-femme", "t-shirts-pyjama-femme", "pantalons-pyjamas-femme"]:
    time.sleep(5)
    main(i)

