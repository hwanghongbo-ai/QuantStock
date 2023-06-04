# coding=utf-8
import numpy as np

from datasource.JueJingDataSource import JueJingDataSource
from service.QuantIndex import QuantIndex
import pandas as pd
from service.QuantFilter import QuantFilter
from datasource.BaoDataSource import BaoDataSource
from config.StockConfig import Freq
from utility.PDTools import PDTools
from utility.QuantTools import QuantTools

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)


jds = JueJingDataSource()
qi = QuantIndex()
qf = QuantFilter()
bao = BaoDataSource()
if __name__ == '__main__':

    # d,dstr=jds.getLatestTradeDate()
    # print(d,dstr)


    start = '2021-09-06'
    end = '2021-10-28'
    symbol = 'SHSE.000001'
    code = 'sz.000001'
    # symbol = 'SHSE.000001'
    # df = jds.getData(symbol=symbol,freq='1d',start=start,end = end,istimeindex=True,isdateformat=True)
    # print(df)

    # # ts = {'hour': 10, 'minute': 30}
    # # # freq = '1800s'
    # data = jds.getData(symbol, Freq.Min_60, start, end, istimeindex=False, isdateformat=False)
    # print(data)
    # time = data['open']
    # time_df = data[['time']]
    # print(data.sort_values(['close'],inplace=False,ascending=False))
    # # print(data.dtypes)
    # print(data.head(2))
    # print(data.tail(1))
    #
    df = bao.getData(code,Freq.Min_60,start,end,istimeindex=False)
    print(df)
    # json,jsonstr = PDTools.toJson(df)
    # print(jsonstr)
    # print(list(json['open'].values()))
    # js = json.loads(jsonstr)
    # open = list(js['open'].values())
    # print( (type(open)))







    # data['volrank'],data['normedrank']=qf.rankvol(data,10)
    # data = qf.candleanalyse(data,['upshadow','downshadow','entity'],True)
    # data = qf.yangxianfanbao(data)
    # print(data)
    # data = jds.getDataWithTS(symbol,ts,start,end)
    # data = qf.pct(data,['close','open','volume','close_ts'])
    # print(data.tail(10))
    # data = qi.rcr(data,9)
    # # print(data.head(20))
    # data.dropna(axis=0, how='any',inplace=True)
    # # print(data.head(20))
    # print(data.close.values.shape)
    # print(data.index.values.shape)
    # print(data.rcr.values.shape)

    # d = qi.rcdr(data,9)
    # print(d)
    # qi.rcvr(data,9)

    # d = qi.supertrend(data)
    # d= qi.psy(data)
    # # d = qi.atr(data,14)
    # d= qi.macd(data)
    # print(d.round(3).tail(5))
    # dd = qf.maxOCHLsInPeriods(data)
    # print(dd)

    # d = qi.myatr(data)
    # print(d)



    # x = data.index.values
    # y= data.close.values
    # r = data.rcr.values
    # # PlotUtility.ShowPlot(x,[r],[symbol],['r'],'date','close',symbol)
    # plt.figure(figsize=(16, 8))
    # plt.subplot(2, 1, 1)
    # plt.plot(x, y, label='close')
    # plt.subplot(2,1,2)
    # plt.plot(x, r, label='rcr')
    # plt.title(symbol)
    # plt.legend()
    # plt.show()

    # PlotUtility.ShowEchart(data,symbol)
    # df = jds.getFundaments('SZSE.300213,SHSE.600089','',start,end)
    # print(df)

    # print(qi.atrExt(data,type='sma'))
    #
    # print('-------------')
    #
    # print(qi.atr(data,isnormalized=False))

    # print(qi.avevolume(data,avetype=1))

    # data['ocd'] = data.close-data.open
    # data['absocd'] = data.ocd.abs()
    # data['sum'] = data.ocd.rolling(9).sum()
    # data['abssum'] = data.ocd.abs().rolling(9).sum()
    # data['absocdsum'] = data.absocd.rolling(9).sum()
    # print(data)

    # test = np.random.randint(0,data.shape[0]-5,size=(5,))
    # print(test,data.shape[0],test.shape)
    # anchor = data.iloc[test]
    # print(anchor)
    # dict = PDTools.FilterDatasAfterPeriods(data,anchor,[2,4])
    # for key in dict.keys():
    #     print('--{}---'.format(key))
    #     print(dict[key])
    # a,b = jds.get_normal_stocks(skip_list_days=30)

    # a,b = QuantTools.getStocks(skip_list_days=20)
    # print(a)
    # print(b)

    # df = QuantTools.getUpperLowLimitPrice(['SZSE.000001'])
    # print(df)








