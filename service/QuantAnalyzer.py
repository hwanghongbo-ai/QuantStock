# coding=utf-8
from service.QuantFilter import QuantFilter
from datasource.QuantDataSourceManager import QuantDataSourceManager
import numpy as np
import matplotlib.pyplot as plt
from utility.PlotUtility import PlotUtility
from utility.PDTools import PDTools
from service.QuantIndex import QuantIndex
import pandas as pd

#原来的QuantTools
'''
本类的作用是进行一些交易数据的相关性分析，特征分析（某特征出现后周期内的概率分析）
'''
class QuantAnalyzer(object):
    # %%
    def __init__(self):

        self.juejingstockdata = QuantDataSourceManager().jueJingDataSource()
        self.filter = QuantFilter()
        self.index = QuantIndex()


    # %%
    def PrintDebug(self, datas):
        printDebug = True
        if printDebug:
            for data in datas:
                print(data)

        # %%
        # 开盘和收盘概率关系，
        # o_pcts , 开盘最高涨幅，最低涨幅，   c_pcts ，收盘涨幅区间
    def p_open2close(self, symbol, o_pcts, c_pcts, start, end=None):
        return self.p_opentime2close(symbol, o_pcts, c_pcts, None, None, start)

        # 开盘和收盘概率关系，
        # o_pcts , 开盘最高涨幅，最低涨幅，   c_pcts ，收盘涨幅区间

    # %%
    def p_time2close(self, symbol, t_pcts, c_pcts, timestamp, start, end=None):
        return self.p_opentime2close(symbol, None, c_pcts, t_pcts, timestamp, start)

    # %%
    # 开盘,某个时刻点（30分钟）和收盘概率关系，
    #o_pcts 开盘区间
    #c_pcts 收盘区间（涨跌幅）
    #t_pcts某时刻区间
    #ts  , 时刻
    def p_opentime2close(self, symbol, o_pcts, c_pcts, t_pcts, ts, start, end=None):

        c_pct_h = c_pcts[1]
        c_pct_l = c_pcts[0]

        if o_pcts != None:
            o_pct_h = o_pcts[1]
            o_pct_l = o_pcts[0]

        if t_pcts != None:
            t_pct_l = t_pcts[0]
            t_pct_h = t_pcts[1]

        #1. 获取数据

        if ts != None:
            data = self.juejingstockdata.getDataWithTS(symbol,ts,start,end)
            fields = ['open','close','close_ts']
        else:
            data = self.juejingstockdata.getData(symbol,'1d',start,end,isresetindex=True)
            fields = ['open', 'close']

        #2. 对数据进行filter 预处理
        data = self.filter.pct(data,fields)

        #3. 数据分析
        if t_pcts == None and o_pcts != None:  # 开盘和收盘概率
            data1 = data[(data['open_pct'] >= o_pct_l) & (data['open_pct'] <= o_pct_h)]
            data2 = data1[(data1['close_pct'] >= c_pct_l) & (data1['close_pct'] <= c_pct_h)]
        elif t_pcts != None and o_pcts == None:  # 时刻和收盘概率
            data1 = data[(data['ts_pct'] >= t_pct_l) & (data['ts_pct'] <= t_pct_h)]
            data2 = data1[(data1['close_pct'] >= c_pct_l) & (data1['close_pct'] <= c_pct_h)]
        elif t_pcts != None and o_pcts != None:
            # print(data)
            data0 = data[(data['open_pct'] >= o_pct_l) & (data['open_pct'] <= o_pct_h)]
            # print(data0)
            data1 = data0[(data0['ts_pct'] >= t_pct_l) & (data0['ts_pct'] <= t_pct_h)]
            # print(data1)
            data2 = data1[(data1['close_pct'] >= c_pct_l) & (data1['close_pct'] <= c_pct_h)]
        else:
            return None

        all = data1.shape[0]
        count = data2.shape[0]
        if all == 0:
            p = 0
        else:
            p = count / all
        self.PrintDebug([data.shape, data1.shape, data1, data2.shape, data2, p, all, count, 'from opentime2close'])
        return p, all, count

        # %%
        # 开盘涨跌幅度对收盘涨跌相关性分析
    def corrbyopen2close(self, symbol, start, end=None,isplot = True):

        # 获取全天
        data = self.juejingstockdata.getData(symbol,'1d',start,end,isresetindex=True,isdateformat=True)
        # 数据预处理，百分数
        data2 = self.filter.pct(data,['open','close'])
        #获取np数据
        npopen = data2.open_pct.values
        npclose = data2.close_pct.values
        # 相关性分析
        oc = np.corrcoef(npclose, npopen, ddof=0)

        self.PrintDebug([npopen, npclose,'相关性open-close：',oc])

        if isplot:
            # 散列图
            plt.figure(figsize=(8, 16))
            plt.subplot(2, 1, 1)
            plt.scatter(x=data2.open_pct, y=data2.close_pct, color='k', s=25, marker="o", label='open-close')
            plt.xlabel('open')
            plt.ylabel('close')
            plt.title(symbol)
            plt.title(symbol)
            plt.legend()
            plt.show()

        return oc

        # %%
        # 分析某个分时收盘和全天收盘的相关性
    def corrbytime2close(self, symbol, timestamp, start, end=None,isplot = True):
        #获取数据
        data = self.juejingstockdata.getDataWithTS(symbol,timestamp,start,end)
        # 数据预处理，百分数
        # data2 = self.filter.pct(data,['open_pct','close_pct','ts_pct'],True)
        data2 = self.filter.pct(data,['close_pct','ts_pct'],True)


        npclose =  data2.close_pct.values
        # npopen=data2.open_pct.values
        npts = data2.ts_pct.values

        # 相关性分析
        # oc = np.corrcoef(npclose, npopen, ddof=0)
        tc = np.corrcoef(npclose, npts, ddof=0)

        # print('相关性open-close：', oc)
        print('相关性ts-close：', tc)

        # 散列图
        if isplot:
            plt.figure(figsize=(8, 16))
            plt.scatter(x=data2.ts_pct, y=data2.close_pct, color='k', s=5, marker="o", label='ts-close')
            plt.xlabel('ts')
            plt.ylabel('close')
            plt.title(symbol)
            plt.legend()
            plt.show()

        return tc

    # %%
    # 开盘涨跌幅度对收盘涨跌相关性分析
    def corrbyVclose2Vol(self, symbol, start, end=None, isplot=True):
        # 获取全天
        data = self.juejingstockdata.getData(symbol, '1d', start, end, isresetindex=True, isdateformat=True)
        # 数据预处理，百分数
        data2 = self.filter.pct(data, ['volume', 'close'])
        # 获取np数据
        npopen = data2.open_pct.values
        npclose = data2.close_pct.values
        # 相关性分析
        oc = np.corrcoef(npclose, npopen, ddof=0)

        self.PrintDebug([npopen, npclose, '相关性open-close：', oc])

        if isplot:
            # 散列图
            plt.figure(figsize=(8, 16))
            plt.subplot(2, 1, 1)
            plt.scatter(x=data2.open_pct, y=data2.close_pct, color='k', s=25, marker="o", label='open-close')
            plt.xlabel('open')
            plt.ylabel('close')
            plt.title(symbol)
            plt.title(symbol)
            plt.legend()
            plt.show()

        return oc

    # %%
    # 分析两个股票的收盘涨跌幅相关性
    def corrbysymbols(self, symbol1, symbol2, start, end=None,isplot = False):

        df1 = self.juejingstockdata.getData(symbol1,'1d',start,end,isresetindex=True,isdateformat=True)
        df2 = self.juejingstockdata.getData(symbol2,'1d',start,end,isresetindex=True,isdateformat=True)

        df1,df2 = PDTools.DropDifferentIndex(df1,df2)

        df1 = self.filter.pct(df1,['close'])
        df2= self.filter.pct(df2,['close'])

        relation = np.corrcoef(df1['close_pct'].values, df2['close_pct'].values, ddof=0)
        print(symbol1,' and ', symbol2, ' 相关性 ' ,relation)
        # draw
        if isplot:
            # x = df1.eob.dt.date.values
            x = df1.index.values
            y0 = np.round(df1['close_pct'].values, 2)
            s0 = symbol1
            y1 = np.round(df2['close_pct'].values, 2)
            # print(type(x), type(y0),type(y1))
            s1 = symbol2
            y = [y0, y1]
            s = [s0, s1]
            c = ['r', 'b']
            PlotUtility.ShowPlot(x, y, s, c, 'date', 'close', 'Close')

        return relation

        # %%
        # 均线的斜率

    def magradient(self, symbol, ma, period, start, end=None):
        data = self.juejingstockdata.getData(symbol, '1d', start, end)
        try:
            data[ma] = data['close'].rolling(ma).mean()
            data.dropna(axis=0, how='any', inplace=True)  # axis=0 ,行， axis=1,列
        except:
            print('Exception: no data')
            return None
        else:
            magradients, madeltas = self.filter.gradients(data[ma].values, period)
            return magradients, madeltas


    # %%
    #macd金叉后
    def riserateonmacdgoldencross(self,symbol,fre,start,end,targetdays,fastperiod=12,slowperiod=26,signalperiod=9):
        data = self.macd(symbol,fre,start,end,fastperiod,slowperiod,signalperiod)
        data = self.filter.macdcross(data)
        data0 = data[data.cross == 1.0]
        # print(data0.shape[0],'+++++++++')
        results =[]
        for targetday in targetdays:
            tdv = pd.DataFrame()
            for item in range(data0.shape[0]):
                ix = data0.iloc[[item]].index.tolist()[0]
                ixd = ix + targetday
                tdv = tdv.append(data.loc[[ixd]])
            # print(ix,ixd)
            # print(data.loc[[ixd]])
            pcts = np.round((tdv.close.values / data0.close.values-1), 2)
            pp = np.array([1 if x >= 0 else 0 for x in pcts])
            dic = {"targetday":targetday,"datas": tdv, "pcts": pcts, "prs": np.round(np.sum(pp) / pp.shape[0], 3)}
            results.append(dic)
            # print(data)
            # print(data0)
            # print(tdv)
            # print(diff)
            # print(pp, type(pp), np.round(np.sum(pp) / pp.shape[0], 3))
        return data, data0, results


    # %%
    #阳线率情况下，后n天的上涨下跌情况及概率
    #返回带有rcn的数据，过滤后满足条件的data，以及targets（天）后的百分数，
    def riserateonrcnr(self,symbol,P,targetdays,start,end,rcrthreshold=1.0):
        data = self.juejingstockdata.getData(symbol,'1d',start,end,isdateformat=True,isresetindex=False)
        data = self.index.rcnr(data,P)
        # data['rcr_1'] = data.rcr.apply(lambda x: 1 if x==1 else 0)
        data0 = data[(data.rcr >= rcrthreshold)]
        results = []
        dict = PDTools.FilterDatasAfterPeriods(source=data, anchors=data0, periods=targetdays)
        for key in dict.keys():
            tdv = dict[key]
            pcts = np.round((tdv.close.values - data0.close.values) / data0.close.values, 2)
            tdv['pcts'] = pcts
            pp = np.array([1 if x >= 0 else 0 for x in pcts])
            dic = {"datas": tdv, "prs": np.round(np.sum(pp) / pp.shape[0], 2)}
            results.append(dic)

        return data,data0,results

    # %%
    #阳线实体和阴线实体占比
    def riserateonrcpr(self,symbol,P,targetdays,start,end,rcprthreshold=1.0):
        data = self.juejingstockdata.getData(symbol, '1d', start, end, isdateformat=True, isresetindex=False)
        data = self.index.rcpr(data, P)
        data0=data[(data['rcpr']>=rcprthreshold)]
        # len = data0.shape[0]
        # print(data0)
        results = []
        # for targetday in targetdays:
        #     tdv = pd.DataFrame()
        #     for item in range(len):
        #         ix = data0.iloc[[item]].index.tolist()[0]
        #         ix = ix + targetday
        #         tdv = tdv.append(data.iloc[[ix]])
        #     # print(pp)
        #     pcts = np.round((tdv.close.values - data0.close.values) / data0.close.values, 2)
        #     pp = np.array([1 if x >= 0 else 0 for x in pcts])
        #     dic = {"datas": tdv, "pcts": pcts, "prs": np.round(np.sum(pp) / pp.shape[0], 3)}
        #     results.append(dic)
        dict = PDTools.FilterDatasAfterPeriods(source=data,anchors=data0,periods=targetdays)
        for key in dict.keys():
            tdv = dict[key]
            pcts = np.round((tdv.close.values - data0.close.values) / data0.close.values, 2)
            tdv['pcts'] = pcts
            pp = np.array([1 if x >= 0 else 0 for x in pcts])
            dic = {"datas": tdv, "prs": np.round(np.sum(pp) / pp.shape[0], 2)}
            results.append(dic)
        return data, data0, results

    # %%
    # 获取macd
    def macd(self, symbol, fre, start, end, fastperiod=12, slowperiod=26, signalperiod=9):
        _start = PDTools.DateAfterOrBeforeSomePeriods(start, 180, True)  # 自动在start日前增加半年数据，确保start时候的macd是正确的
        data = self.juejingstockdata.getData(symbol, fre, _start, end)
        macddata = QuantIndex.macd(data, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        macddata.dropna(axis=0, how='any', inplace=True)
        macddata = macddata[macddata.time >= start]  # 取消为了macd正确而加的冗余日期
        macddata = macddata.round(3)
        return macddata

    # %%
    #获取一个周期内，针对ma均线的最大或最小乖离率的值所对应的K线数据
    def maxminbias(self,symbol,fre,ma,ismax,start,end):
        data = self.juejingstockdata.getData(symbol,fre,start,end)
        try:
            data['ma'] = data['close'].rolling(window=ma).mean()
            # data.dropna(axis=0, how='any', inplace=True)  # axis=0 ,行， axis=1,列
        except:
            print('Exception: no data')
            return None
        data['bias'] = (data['close'] / data['ma']-1)*100
        if ismax:
            arg = data['bias'].argmax()
        else:
            arg = data['bias'].argmin()
        # print(data.head(10))
        # print(arg)
        return data.iloc[[arg]]  #返回dataframe， data.iloc[arg]返回series

    '''
     symbol1fb['pctdif'] 收盘价百分比的一阶差分
     symbol1fb['pctdifsum'] 收盘价百分比的一阶差分累积和
    '''
    def pctdiffbytwosymbols(self,symbol1,symbol2,fre,start,end=None):
        symbol1fb = self.juejingstockdata.getData(symbol1,fre,start,end,isdateformat=True)
        symbol2fb = self.juejingstockdata.getData(symbol2,fre,start,end,isdateformat=True)
        symbol1fb = self.filter.pct(symbol1fb,['close'],False)
        symbol2fb = self.filter.pct(symbol2fb,['close'],False)
        symbol1fb['pctdif'] = symbol1fb['close_pct']-symbol2fb['close_pct']
        symbol2fb['pctdif'] = -1* symbol1fb['pctdif']
        symbol1fb['pctdifsum'] = symbol1fb['pctdif'].cumsum()
        symbol2fb['pctdifsum'] = symbol2fb['pctdif'].cumsum()

        # print(symbol1fb.tail(10))
        # print(symbol2fb.tail(10))
        return symbol1fb,symbol2fb

    #大阳线后第二天低开，走势分析
    def dayangdikai(self,symbol,fre,yangvalue,openvalue,targetdays,start,end):
        data = self.juejingstockdata.getData(symbol,fre,start,end,isdateformat=True)
        data = self.filter.pct(data,['close','open'],True)
        data['pre_closepct'] = data['close_pct'].shift(1)
        dayangdf = data[(data['pre_closepct']>=yangvalue) & (data['open_pct']< openvalue )]
        # print(dayangdf)
        # print('---------')
        dict = PDTools.FilterDatasAfterPeriods(source=data, anchors=dayangdf, periods=targetdays)
        return dict,dayangdf


    # #阳线反包，n天后下跌概率分析
    # def  yangxianfanbao(self,symbol,freq,targetdays,start,end):
    #     data = self.juejingstockdata.getData(symbol,freq,start,end)
    #     tempd = self.yangxianfanbao(data




















