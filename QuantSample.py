# coding=utf-8
from service.QuantAnalyzer import QuantAnalyzer
import pandas as pd
from service.QuantIndex import QuantIndex
from service.QuantFilter import QuantFilter
from datasource.JueJingDataSource import JueJingDataSource
from datasource.JueJingDataSource import TimeColumnName
from render.EchartRender import EchartRender
from render.EchartRender import YAxisInfo
import numpy as np
from datasource.WormsDataSource import WormsDataSource
from database.DBHelper import MySQLHelper
from config.StockConfig import Freq
from datasource.BaoDataSource import BaoDataSource
from datasource.HbDataSource import HbDataSource
from config.StockConfig import Exchange
from utility.QuantTools import QuantTools

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)

from render.EchartRender import FigurePath

def echarttest():
    jds = JueJingDataSource()
    data = jds.getData(symbol, '1d', start, end, isresetindex=False, isdateformat=True)
    data = qi.sma(data, [5, 10, 20])
    data = qi.macd(data)
    # print(data[jds.timeColumeName()])
    # PlotUtility.ShowEchart(data,symbol)
    # qi.rcnr(data,P=5)
    # # print(data)
    left = 80
    right = 50


    echart.setXAxisData(data[TimeColumnName].values.tolist())
    yaixsinfo = YAxisInfo()
    yaixsinfo.yaxisdata = data.volume.values.tolist()
    ochl = data[['open', 'close', 'high', 'low']]
    bardata = ochl.values.tolist()
    madf = data[['SMA5', 'SMA10', 'SMA20']]
    echart.drawKLine(ochldf=ochl, madf=madf, left=left, right=right, top=50, height=300, seriesname="", maintitle="日线走势", subtitle=symbol)
    echart.drawVolumeBar(data.volume.values.tolist(), bardata=bardata, left=left, right=right, top=400, height=80)
    echart.drawMacdBar(data.DIF.values.tolist(), data.DEA.values.tolist(), data.HIST.values.tolist(), left=left,
                       right=right, top=500, height=100)

    # echart.drawLine([yaixsinfo],left=80,right=50,top=150,height=200,isshowxvalue=True,maintitle="成交量",subtitle=symbol)
    # echart.drawBar([yaixsinfo],left=50,right=50,top=150,height=200,isshowxvalue=True,isshowyvalue=False,maintitle="成交量",subtitle=symbol)
    # echart.drawLine(data.rcr.values.tolist(),gridtop='310px',gridheight='60px')

    echart.render("{}hhb.html".format(FigurePath))

def macdtest():
    # macddata = qts.macd(symbol,'1d',start,end)
    # qts.macdcross(symbol,'1d',start,end)
    # print(macddata)
    # d,gd = qf.macdgoldencross(macddata,isdifgrow=True,isdeagrow=False,trendhalfperiod=3, macdthreshold=-0.2,pthreshold=5,vthreshold=0.12)
    # # print(d)
    # print('++++++++++++++++++++++++++')
    # print(gd)
    data, data0, results = qts.riserateonmacdgoldencross(symbol,'1d',start,end,[3,5])
    print(data)
    print(data0)
    print(results)
    # qf.macddifdeatrend(macddata,250,3)

def probofopenverclose():
    oo=[2,99]
    cc=[2,99]
    qts.p_open2close(symbol,oo,cc,start,end)


def corrofopenverclose():
    qts.corrbyopen2close(symbol,start,end)
    oo = [0,99]
    cc= [2,99]
    tt = [4,99]
    ts = {'hour': 10, 'minute': 00}
    qts.p_opentime2close(symbol,oo,cc,tt,ts,start,end)

def corrby2symbols():
    s1= 'SZSE.300809'
    s2= 'SZSE.300083'
    # qts.corrbysymbols(s1,s2,'2021-10-11',isplot=True)
    qts.corrbysymbols(s1, s2, '2020-01-01',isplot=True)
    # qts.riserateonrcr(s1,5,2,start,None)

def maxminbias():
    df = qts.maxminbias(symbol='SHSE.000001',fre='1d',ma=120,ismax=True,start='2010-01-01',end=None)
    print(df)

def magradients():
    magradients,madeltas = qts.magradient(symbol='SZSE.000661',ma=5,period=5,start='2021-09-13',end='2021-10-14')
    print('5日均线，5日周期梯度：')
    print(magradients)
    print(madeltas)

def pctdiffbytwosymbols():
    data,s2 = qts.pctdiffbytwosymbols(symbol,index,'1d',start,end)
    data['pctma'] = data['pctdifsum'].rolling(5).mean()
    print(data.tail(10))
    print(s2.tail(10))
    echart.setXAxisData(data[JueJingDataSource.GetTimneColumnName()].values.tolist())
    ochl =data[['open', 'close', 'high', 'low']]
    left = 80
    right = 50
    echart.drawKLine(ochldf=ochl, madf=None, left=left, right=right, top=50, height=300, seriesname="",   maintitle="日线走势", subtitle=symbol)
    yaixsinfo = YAxisInfo()
    yaixsinfo.yaxisdata = np.round(data.pctdifsum.values,2).tolist()
    yaixsinfoma = YAxisInfo()
    yaixsinfoma.yaxisdata = np.round(data.pctma.values,2).tolist()
    echart.drawLine([yaixsinfo,yaixsinfoma],left,right,top=400,height=120,isshowxvalue=True)
    echart.render('{}pctdiff.html'.format(FigurePath))

def dayangdikaitest():
    dict,dayangdf = qts.dayangdikai(symbol,'1d',5,-3,[0,1,2,3,4,5,6,7,8,9],start,None)
    for key in dict.keys():
        print(key)
        print(dict[key])

    print(dayangdf)



def beixiangtest():
    wd = WormsDataSource()
    # df = wd.wormBeiXiangEx(type='S',start='2022-02-21',end=None)
    # print(df)
    # print(df[['HOLD_DATE']],type(df[['HOLD_DATE']]))
    # print((df['HOLD_DATE'].iloc[0]))
    # print(type(df.iloc[[0]]),df.iloc[[0]])
    df = wd.wormBeiXiang()
    print(df)

def zjlxtest():
    wd = WormsDataSource()
    df =wd.zjlx('zs000001')
    # df = wd.zjlx('BK0722')
    print(df)

def bkcodenamemap():
    wd = WormsDataSource()
    df = wd.bknamecodemap(type='GN')
    print(df)

def avePEtest():
    wd = WormsDataSource()
    sh = '000001'
    cy = '399006'
    hs300='000300'
    sz50='000016'  # 没有上证50
    df = wd.peavg(symbol=hs300,datastart='2022-01-01',start='2022-03-01',end=None)
    print(df)


def dailyupdownstop():
    wd = WormsDataSource()
    df = wd.dailyupdownstop(type='zt')
    print(df)

def dailyUpDownInfos():
    wd = WormsDataSource()
    df = wd.dailyUpDownInfos()
    print(df)


def dbhelpertest():
    sql = MySQLHelper()
    # print('--id:{}\n--id:{}'.format(id(sql),id(sql1)) )
    print('--id:{} '.format(id(sql) ))
    # rt = sql.select("select * from beixiang")
    # print(rt)
    del sql
    sql = None
    sql1 = MySQLHelper()
    print('--id:{}'.format(  id(sql1)))
    del sql1


def quatadatasourcetest():
    qds = HbDataSource()
    # d,c =qds.getBeixiangData(start='2022-03-01',end='2022-03-10',retcolums=True)
    # print(d)
    # print(c)
    # df = pd.DataFrame(data=d,columns=c)

    df = qds.getBeixiangDataByPD(start='2022-02-15',end='2022-03-01')
    print(df)

    # count = qds.getUpDownStopCount(type='upstopopen')
    # print(count)

    # df = qds.getUpdownInfos()
    # print(df)

    # df = qds.getAvgPEdata('000001',start='2021-03-05')
    # print(df)

    # df = qds.getContinuousUpStopSymbols(date='2022-04-18',days=3)
    # print(df)

    # df = qds.getHighestUpStopDays()
    # print(df)

def baotest():
    bao=BaoDataSource()
    symbol = Exchange.Symbol(Exchange.Bao_SHANGHAI,'000001')
    print(symbol)
    freq = Freq.Week
    df = bao.getData(symbol,freq,start,end)
    print(df)
    print(df.dtypes)
    bao.disconnect()

def allstocks():
    QuantTools.getStocks(Exchange.Jue_SHENGZHENG,)


def smatest():
    bao = BaoDataSource()
    symbol = Exchange.Symbol(Exchange.Bao_SHANGHAI, '000001')
    freq = Freq.Day
    df = bao.getData(symbol, freq, start, end)
    qi.sma(data=df,maperiods=[5,10])
    print(df)
    # print(df.dtypes)
    bao.disconnect()


qts = QuantAnalyzer()
qf = QuantFilter()
qi = QuantIndex()
start = '2020-12-01'
end = '2021-11-01'
# symbol = 'SZSE.300213'
symbol = 'SHSE.600089'
# symbol = 'SHSE.600699'
index = 'SHSE.000001'

echart = EchartRender()

if __name__ == '__main__':


##开盘和收盘概率关系，
    # probofopenverclose()

#开盘收盘相关性分析
    # corrofopenverclose()

#两股票收盘价相关性分析
    # corrby2symbols()

#macd
    # macdtest()

    #斜率
    # magradients()

    # maxminbias()



    #反包
    # data =qts.fanbao(symbol,'1d',5,start,end)
    # print(data)

    #ECharter
    # echarttest()

    # pctdiffbytwosymbols()

    #大阳线后第二日低开，当日及几日后的涨跌概率
    # dayangdikaitest()

     # 北向
     # beixiangtest()

 #资金流向
    zjlxtest()

#bk code name map
    # bkcodenamemap()

#create table
    # createTable()


 # 平均市盈率
 #    avePEtest()

#每日涨跌停数据
    # dailyupdownstop()

#每日涨跌详细信息
    # dailyUpDownInfos()

#DB TEST
    # dbhelpertest()

#quatadatasource test
    # quatadatasourcetest()

#Bao Test
    # baotest()

#sma test
    # smatest()















