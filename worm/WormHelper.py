# coding=utf-8
from selenium import webdriver  #导入模块
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from pyquery import PyQuery as pq
import json

import time
from lxml import etree
from os import path


import re


class WormHelper(object):
    def __init__(self):
        d = path.dirname(__file__)
        self.chromedriverpath = path.join(d, 'chromedriver.exe')
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('–headless')
        # option.add_argument("--mute-audio")  # 静音
        # option.add_argument('–no - sandbox')
        # option.add_argument('–disable - dev - shm - usage')
        # option.binary_location = chromedriverpath

    #use pyquery worm json data to df
    def wormJson(self, url, keys, root):
        print("\n{}".format(url))
        doc = pq(url)
        source = doc.html()
        dic = json.loads(source)
        for i in root:
            dic = dic[i]
        fields = dic
        # print(fields )
        dflist = []
        if isinstance(fields,dict):
            lst = self.__parsedict(field=fields,keys=keys)
            dflist.append(lst)
        elif isinstance(fields,list):
            for field in fields:
                # print(field['HOLD_DATE'],field['ADD_MARKET_CAP'])
                lst = self.__parsedict(field=field, keys=keys)
                dflist.append(lst)
        df = pd.DataFrame(dflist, columns=keys)
        return df


    def wormPageBySelenium(self,url,xpath,callbackfunc):
        print(url)
        dflist = []
        try:
            driver = webdriver.Chrome(self.chromedriverpath, options=self.option)
            wait = WebDriverWait(driver, 10)
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            time.sleep(0.5)
            source = driver.page_source
            mytree = etree.HTML(source)
            items = mytree.xpath(xpath)  # tbody下所有tr标签
            for item in items:
                lst = callbackfunc(item)
                dflist.append(lst)

            # time.sleep(0.5)
            driver.close()
            print('driver closed')
        except Exception as e:
            print(e)
        return dflist

    def __parsedict(self,field,keys):
        lst = []
        for key in keys:
            lst.append(field[key])
        return lst

