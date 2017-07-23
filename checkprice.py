# !/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import json
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

URL="https://online.nojima.co.jp/category/10006902/?searchCategoryCode=10006902&mode=image&pageSize=15&currentPage=1&alignmentSequence=1&searchDispFlg=true&attributeValue=0_1&attributeValue=0_2&attributeValue=1_6&attributeValue=2_3&searchPriceRange=10000-14999"
USERAGENT = "Mozilla/5.0"
pb = Pushbullet("")


class CheckPrice():
    
    def __init__(self):
        pass

    def main(self):
        info = {}
        info = self.ExtractInfo(URL)
        if len(info) == 0:
            #pb.push_note("お知らせ","更新なし")
            pass
        else:
            content = json.dumps(info, ensure_ascii=False, indent=4)
            pb.push_note("お知らせ",content)
            #print (content)

    def ProcessingHTTP(self,url):
        req = urllib.request.Request(url)
        req.add_header('User-agent',USERAGENT)
        res = urllib.request.urlopen(req)
        html = res.read()
        return html

    def ArrangeInfo(self,info,carrier,name,storage,color,price,count):
        if count not in info:
            info[count] = []
        contents = info[count]
        contents.append({"carrier":carrier})
        try:
            content = contents[-1]
            content["name"] = name
            content["storage"] = storage
            content["color"] = color
            content["price"] = price
        except:
            pass

    def ExtractInfo(self,url):
        count = 0
        info = {}
        text = []
        html = self.ProcessingHTTP(url)
        soup = BeautifulSoup(html,"html.parser")
        for a in soup.findAll("div",attrs={"class":"commoditylistitem"}):
            for b in a.findAll('li'):
                text = (b.text.split())
                name = (text[4])
                if "iPhone6" not in name:
                    continue
                carrier = (text[3])
                storage = (text[5])
                color = (text[6])
                price = (text[8])
                count = count + 1
                self.ArrangeInfo(info,carrier,name,storage,color,price,count)
        return info
                
if __name__ == "__main__":
    checkprice = CheckPrice() 
    checkprice.main()
