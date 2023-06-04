import numpy as np
from flask import Blueprint
from service.StockData import StockData
import pandas as pd
from service.QuantIndex import QuantIndex
from utility.PDTools import PDTools
from config.StockConfig import Freq
from config.StockConfig import Echart_OCHL

stat = Blueprint('stat',__name__)


#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)

sd = StockData()



@stat.route('/risefalldetail/<fields>/<startdate>/<enddate>')
def risefalldetail(fields,startdate,enddate):
    print(fields,startdate,enddate)
    start = None
    end = None
    if startdate != 'none':
        start = startdate
    if enddate != 'none':
        end = enddate
    df = sd.getRiseFallDetails(fields=fields,start=start,end=end)
    print(df)
    # print(df.info())
    return PDTools.toJsonbyColumn(df)

@stat.route('/risefallratio/<startdate>/<enddate>')
def risefallratio(startdate,enddate):
    if startdate is None or enddate is None:
        return {}
    code = 'SHSE.000001'
    df = sd.getRiseFallDetails(fields='trade_date,rise_num,fall_num',start=startdate,end=enddate)
    df = QuantIndex.risefallratio(df)
    df = QuantIndex.sma(data=df,maperiods=[10],columns=['ratio']).fillna(0)
    df1 = sd.getShortPeriodData(symbol=code,freq=Freq.Day,start=startdate,end=enddate)
    df.set_index('trade_date',inplace=True)
    df1.set_index('time',inplace=True)
    df=pd.concat([df,df1[Echart_OCHL]],axis=1)
    df.sort_index(inplace=True,axis=0,ascending=True)
    print(df)
    return {'code': code,'trade_date':df.index.values.tolist(),'ratio':df.ratio.values.tolist(),'values':df[Echart_OCHL].values.tolist()}

@stat.route('/beixiang/<startdate>/<enddate>')
def beixiang(startdate,enddate):
    df = sd.getBeixiangDatas(fields="HOLD_DATE,HOLD_MARKET_CAP",start=startdate,end=enddate)
    df['HOLD_MARKET_CAP'] = df['HOLD_MARKET_CAP']/100000000
    # code = 'SHSE.000001'
    code = 'SHSE.000300'
    df1 = sd.getShortPeriodData(symbol=code, freq=Freq.Day, start=startdate, end=enddate)

    df.set_index('HOLD_DATE', inplace=True)
    df1.set_index('time', inplace=True)
    df = pd.concat([df, df1[Echart_OCHL]], axis=1)
    df.sort_index(inplace=True,axis=0,ascending=True)  #ascending=False  倒序
    print(df)
    cap = df['HOLD_MARKET_CAP'].values
    caplist = np.where(np.isnan(cap))
    for i in caplist[0]:
        if i == 0:
            cap[i] = 0
        else:
            cap[i] = cap[i-1]
    print(cap.tolist())
    return {'code': code,'trade_date':df.index.values.tolist(),'beixiang':cap.tolist(),'values':df[Echart_OCHL].values.tolist()}

