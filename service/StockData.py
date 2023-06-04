# coding=utf-8
from datasource.QuantDataSourceManager import QuantDataSourceManager
from datasource.JueJingDataSource import JueJingDataSource
from datasource.BaoDataSource import BaoDataSource
from datasource.HbDataSource import HbDataSource
import pandas as pd
from config.StockConfig import Freq

class StockData(object):
    def __init__(self):
        quantdatasourcemanager = QuantDataSourceManager()
        self.juejing = quantdatasourcemanager.jueJingDataSource()
        self.bao = quantdatasourcemanager.baoDataSource()
        self.hb = quantdatasourcemanager.hbDataSource()
        pass

    #短周期分钟级别或日线级别，使用掘金
    def getShortPeriodData(self,symbol,freq,start,end=None,istimeindex=False):
        isdataformat = True
        if freq < Freq.Day:
            isdataformat = False
        df = self.juejing.getData(symbol=symbol,freq=freq,start=start,end=end,istimeindex=istimeindex,isdateformat=isdataformat)
        # df['time'] = df.time.dt.strftime('%Y-%m-%d')
        return df

    # 周线或月线级别，使用bao
    def getLongPeriodData(self,symbol,freq,start,end=None,istimeindex=False):
        return self.bao.getData(code=symbol,freq=freq,start_date=start,end_date=end)

    # 获取指定日期的涨跌信息数据
    def getRiseFallDetails(self,fields,start=None,end=None):
        if fields != "*" and fields.find('trade_date') == -1:
            fields = ",".join(['trade_date', fields])
        df =  self.hb.getRiseFallDetails(field=fields,start=start,end=end)
        df['trade_date'] = df['trade_date'].dt.strftime('%Y-%m-%d')
        return df


    def getBeixiangDatas(self,fields=None,start=None,end=None):
        df = self.hb.getBeixiangData(fields=fields,start=start,end=end)
        df['HOLD_DATE']=df['HOLD_DATE'].dt.strftime('%Y-%m-%d')
        return df







