# coding=utf-8

import pandas as pd
import numpy as np

import re
from worm.WormHelper import WormHelper

 # query data to DF by worm
class WormsDataSource(object):
    def __init__(self):
        self.worm = WormHelper()

    def wormBeiXiangEx(self,type="",pagesize="",page=1,start=None,end=None):
        BeiXiangDataURL = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=HOLD_DATE&sortTypes=1&pageSize={}&pageNumber={}&columns=ALL&reportName=RPT_MUTUAL_MARKET_STA"
        BeiXiangDataHGTURL = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=HOLD_DATE&sortTypes=1&pageSize={}&pageNumber={}&columns=ALL&reportName=RPT_HMUTUAL_MARKET_STA"
        BeiXiangDataSGTURL = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=HOLD_DATE&sortTypes=1&pageSize={}&pageNumber={}&columns=ALL&reportName=RPT_SMUTUAL_MARKET_STA"
        # sortTypes =1：正序 ；sortTypes = -1：倒序
        keys=['HOLD_DATE', 'CHANGE_RATE', 'ADD_MARKET_CAP', 'ADD_MARKET_RATE', 'HOLD_MARKET_CAP', 'HOLD_MARKET_RATE',
            'ADD_MARKET_BNAME', 'ADD_MARKET_NEWBCODE','BOARD_RATE_BNAME','BOARD_RATE_NEWBCODE','MARKET_RATE_BNAME', 'MARKET_RATE_NEWBCODE',
            'ADD_MARKET_MCODE', 'ADD_MARKET_MNAME', 'ADD_SHARES_MCODE', 'ADD_SHARES_MNAME', 'MARKET_RATE_MCODE', 'MARKET_RATE_MNAME']
        if type == "hgt":
            url = BeiXiangDataHGTURL.format(pagesize,page)
        elif type == "sgt":
            url = BeiXiangDataSGTURL.format(pagesize,page)
        else:
            url = BeiXiangDataURL.format(pagesize,page)
        df = self.worm.wormJson(url,keys,['result','data'])
        df['HOLD_DATE']= df['HOLD_DATE'].str[:10]
        df['CHANGE_RATE']=np.round(df['CHANGE_RATE'],2)
        df['ADD_MARKET_CAP'] = np.round(df['ADD_MARKET_CAP'], 0)
        df['ADD_MARKET_RATE'] = np.round(df['ADD_MARKET_RATE']*1000, 2)
        df['HOLD_MARKET_CAP'] = np.round(df['HOLD_MARKET_CAP'], 0)
        df['HOLD_MARKET_RATE'] = np.round(df['HOLD_MARKET_RATE']*100, 2)
        # print(df)

        if not(start is None):
            df = df[df['HOLD_DATE'] >= start]

        if not(end is None):
            df = df[df['HOLD_DATE'] <= end]
        return df


    def wormBeiXiang(self,start=None,end=None):
        BeiXiangURL = "https://data.eastmoney.com/hsgtcg/gzcglist.html"
        xpath=r"//*[@id='dataview']/div[2]/div[2]/table/tbody/tr"
        def handler(item):
            fields = item.xpath("./td") #当前tr下所有td标签
            lst =[]
            for field in fields:
                lst.append(field.xpath(".//text()")[0])
            return lst
        dflist = self.worm.wormPageBySelenium(url=BeiXiangURL,xpath=xpath, callbackfunc=handler)
        print(dflist)
        # df = pd.DataFrame(dflist,columns=['日期', '300涨跌', '增持市值', '增持市值占比', '市值', '市值占比', '最大增持市值板块',
        #                            '占板块比增加', '占全市场比增加', '最大增持市值个股', '最大增持股数个股', '占股比增加'])
        df = pd.DataFrame(dflist, columns=['date', 'pct', 'zcsz', 'zcszzb', 'zsz', 'zszzb', 'zdzcbk','zbkbzj', 'zqscbzj', 'zdzcszgg', 'zdzcgsgg', 'zgbzj'])
        return df


#资金流向
    #code :
    # 沪市： zs000001； 深市：zs399001； 创业板：zs399006  ; 板块：BKxxxx BK0629北斗板块
    def zjlx(self,code,isformat=True,start=None,end=None):
        isbkzj = False
        if code[:2]=="BK":
            isbkzj = True
        if isbkzj:
            url = "https://data.eastmoney.com/bkzj/{}.html".format(code)
        else:
            url = "https://data.eastmoney.com/zjlx/{}.html".format(code)

        xpath = r"// *[ @ id = 'table_ls'] / table / tbody / tr"
        def handler(item):
            fields = item.xpath("./td")  # 当前tr下所有td标签
            lst = []
            for field in fields:
                lst.append(field.xpath(".//text()")[0])
            return lst
        dflist = self.worm.wormPageBySelenium(url=url,xpath=xpath,callbackfunc=handler)
        print(dflist)
        if isbkzj:    #11个字段
            df = pd.DataFrame(dflist,
                              columns=['time', 'cap_flowin_amt', 'cap_flowin_rate', 'super_flowin_amt',
                                       'super_flowin_rate',
                                       'huge_flowin_amt', 'huge_flowin_rate', 'middle_flowin_amt', 'middle_flowin_rate',
                                       'small_flowin_amt', 'small_flowin_rate'])
        else:  #13个字段
            df = pd.DataFrame(dflist,columns=['time', 'close', 'pct', 'cap_flowin_amt', 'cap_flowin_rate', 'super_flowin_amt','super_flowin_rate',
                        'huge_flowin_amt', 'huge_flowin_rate', 'middle_flowin_amt', 'middle_flowin_rate', 'small_flowin_amt','small_flowin_rate'])

        if not (start is None):
            df = df[df['HOLD_DATE'] >= start]

        if not (end is None):
            df = df[df['HOLD_DATE'] <= end]

        if isformat:
            # df['pct']=df['pct'].str[:-1]
            def formathandle(x):
                if not isbkzj:
                    x['pct'] = x['pct'][:-1]
                x['cap_flowin_amt'] = x['cap_flowin_amt'][:-1]
                x['cap_flowin_rate'] = x['cap_flowin_rate'][:-1]
                x['super_flowin_amt'] = x['super_flowin_amt'][:-1]
                x['super_flowin_rate'] = x['super_flowin_rate'][:-1]
                x['huge_flowin_amt'] = x['huge_flowin_amt'][:-1]
                x['huge_flowin_rate'] = x['huge_flowin_rate'][:-1]
                x['middle_flowin_amt'] = x['middle_flowin_amt'][:-1]
                x['middle_flowin_rate'] = x['middle_flowin_rate'][:-1]
                x['small_flowin_amt'] = x['small_flowin_amt'][:-1]
                x['small_flowin_rate'] = x['small_flowin_rate'][:-1]
                # print(x['pct'],x['cap_flowin_amt'],x['cap_flowin_rate'],x['super_flowin_amt'] , x['super_flowin_rate'],x['huge_flowin_amt'])
                return x
            df = df.apply(lambda x:formathandle(x),axis=1)
        return df

    # /html/body/div[1]/div[8]/div[2]/div[2]/div[2]/div/div/div/div[3]/div[2]/a[1]
    # / html / body / div[1] / div[8] / div[2] / div[2] / div[2] / div / div / div / div[3] / div[3] / a[1]
    def bknamecodemap(self,type='BK'):
        url = "https://data.eastmoney.com/bkzj/{}.html".format('BK0433')

        if type == 'BK':
            t = 2
        elif type == 'GN':
            t = 3

        xpath = "/html/body/div[1]/div[8]/div[2]/div[2]/div[2]/div/div/div/div[3]/div[{}]/a".format(t)
        def handler(item):
            lst = []
            m = re.findall(pattern="BK\d+", string=item.xpath("./@href")[0])
            lst.append(m[0])
            lst.append(item.xpath(".//text()")[0])
            return lst
        dflist = self.worm.wormPageBySelenium(url=url,xpath=xpath,callbackfunc=handler)
        df = pd.DataFrame(dflist,columns=['bkcode', 'bkname'])
        return df

    #symbol: 000001 sh, 399001 sz, 399006 cy
    def peavg(self,symbol,datastart,pagesize="",page=1,sorttype=1,start=None,end=None):
        url="https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=TRADE_DATE&sortTypes={}&pageSize={}&pageNumber={}&reportName=RPT_VALUEMARKET&columns=ALL&filter=(TRADE_MARKET_CODE%3D%22{}%22)(TRADE_DATE%3E%27{}%27)".format(sorttype,pagesize,page,symbol,datastart)
        keys = ['TRADE_DATE', 'CLOSE_PRICE', 'CHANGE_RATE', 'TOTAL_SHARES', 'FREE_SHARES', 'TOTAL_MARKET_CAP',
                'FREE_MARKET_CAP', 'PE_TTM_AVG']

        df = self.worm.wormJson(url=url,keys=keys,root=['result','data'])
        # print("result:{},page:{},count:{},len:{}".format(dict['success'], dict['result']['pages'], dict['result']['count'],len(fields)))
        # print(url)
        df['TRADE_DATE'] = df['TRADE_DATE'].str[:10]
        df['CLOSE_PRICE'] = np.round(df['CLOSE_PRICE'], 2)
        df['CHANGE_RATE'] = np.round(df['CHANGE_RATE'], 2)
        # df['ADD_MARKET_RATE'] = np.round(df['ADD_MARKET_RATE'] * 1000, 2)
        # df['HOLD_MARKET_CAP'] = np.round(df['HOLD_MARKET_CAP'], 0)
        # df['HOLD_MARKET_RATE'] = np.round(df['HOLD_MARKET_RATE'] * 100, 2)
        # print(df)

        if not (start is None):
            df = df[df['TRADE_DATE'] >= start]

        if not (end is None):
            df = df[df['TRADE_DATE'] <= end]
        return df


    def jigouchichangzhanbi(self,symbol):
        pass

#当日涨跌停
    #type = zt:涨停， dt:跌停， zb：炸板， lb：连办
    def dailyupdownstop(self,type):
        if type=='zt':
            pool = 'up_pool'
        elif type=='dt':
            pool = 'down_pool'
        elif type=='zb':
            pool = 'up_open_pool'
        elif type=='lb':
            pool = 'continuous_up_pool'
        url = "https://x-quote.cls.cn/quote/index/up_down_analysis?rever=1&sv=7.7.5&type={}&way=last_px".format(pool)
        if type == 'dt' or type=='zb':
            keys = ["secu_code", "secu_name", "last_px", "time", "num_stocks"]
        else:
            keys=["secu_code","secu_name","last_px","time","num_stocks","limit_up_days"]
        df = self.worm.wormJson(url,keys,['data'])
        # print(df)
        return df

    # 当日涨，跌，停牌家数详细信息，以及-10,8,6,4,2,0,2,4,6,8,10左右的家数
    def dailyUpDownInfos(self):
        url = r"https://x-quote.cls.cn/quote/index/home"
        root=["data","up_down_dis"]
        keys=["rise_num","fall_num","suspend_num","up_num","down_num","down_10","down_8","down_6","down_4","down_2","flat_num","up_2","up_4","up_6","up_8","up_10"]
        df = self.worm.wormJson(url=url,keys=keys,root=root)
        # print(df)
        return df




if __name__ == '__main__':
    worms = WormsDataSource();
    df = worms.bknamecodemap()
    print(df)























