# coding=utf-8
import numpy as np
import talib as tb
import statsmodels.api as sm
import pandas as pd
from config.StockConfig import TimeColumnName

'''
本类是自定义的一些技术指标或者通过talib获取技术指标，用于数据分析
'''


class QuantIndex(object):
    def __init__(self):
        pass



    @staticmethod
    def sma(data,maperiods,columns=['close']):

        for maperiod in maperiods:
            for column in columns:
                data[column+'_SMA'+str(maperiod)] = np.round(tb.SMA(data[column], timeperiod=maperiod),2)
        return data

    @staticmethod
    def ema(data,maperiods,columns=['close']):
        for maperiod in maperiods:
            for column in columns:
                data[column+"_EMA" + str(maperiod)] = tb.EMA(data[column], timeperiod=maperiod)
        return data


    @staticmethod
    #一般以当前日期前推>=5个月作为start，这当前日期的macd数据比较接近东方财富
    #比如，要计算2021-10-8日的macd，可以从2021-05-08或以前作为start
    def macd(data, fastperiod=12,slowperiod=26,signalperiod=9):
        #  DIF=EMA（fastperiod）－EMA（slowperiod）  DIF组成的线叫做MACD线
        #  DEA = signalperiod 天的 DIF的EMA(移动平均线）  DEA组成的线叫做Signal线,
        #  MACD signal 2x(DIF - DEA)  --> macd柱线 2×（DIF-DIF的9日加权移动均线DEA）得到MACD柱
        dif, dea, macdhist = tb.MACD(data['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        data['DIF'] = dif
        data['DEA'] = dea
        data['HIST'] = macdhist*2
        return data

    @staticmethod
    def boll(data,timeperiod=20,matype=0,stdup=2,stddn=2):
        ''''
        中轨线=timeperiod日的移动平均线(matype)
        上轨线=中轨线+stdup倍的标准差
        下轨线=中轨线－stddn倍的标准差（K为参数，可根据股票的特性来做相应的调整，一般默认为2）
        '''
        data['upper'], data['middle'], data['lower'] = tb.BBANDS(
               data.close.values,
               timeperiod=timeperiod,
               # number of non-biased standard deviations from the mean
               nbdevup=stdup,
               nbdevdn=stddn,
               # Moving average type: simple moving average here
               matype=matype)
        return data

    # ATR上真实波幅
    # TR: MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW));
    # ATR: MA(TR, N)
    # isnormalized 是否归一化
    @staticmethod
    def atr(data, timeperiod=14, isnormalized=False):
        if isnormalized:
            data['atr'] = tb.NATR(data.high.values, data.low.values, data.close.values, timeperiod)
        else:
            data['atr'] = tb.ATR(data.high.values, data.low.values, data.close.values, timeperiod)
        return data


   #ewm ( 加权滑动窗口）
    # EWM公式：
    # Y(k) = α* X(K)+ (1-α)*Y(k-1)
    # com：根据质心指定衰减， α = 1 / (1 + com),  for com≥0
    # span ：根据范围指定衰减， α = 2 / (span + 1),for span≥1  ---> 这个就是一般用的，如macd，26， 2/27*X(1)+25/27*macd(1)
    # halflife ：根据半衰期指定衰减， α = 1−exp(log(0.5) / halflife), forhalflife > 0
    # alpha：直接指定平滑系数α， 0 < α≤1。
    # min_periods ：窗口中具有值的最小观察数

    #EMA公式
    #若Y(K)=EMA(X(K)，N)，则Y=［2*X(K)+(N-1)*Y(K-1)]/(N+1)，其中Y(K-1)表示前一日的EMA， Y(K-1)= EMA(X(K-1),N)
    #可见EMA其实就是ewm公式中span的那种情况

    @staticmethod
    def atrExt(data,timeperiod=14,type='ewm'):
        # tempdf=data[['high','low','close',TimeColumnName]]
        tempdf = pd.DataFrame(data,columns=['high','low','close',TimeColumnName]) # 这样不会警告
        tempdf['pre_close'] = tempdf.close.shift(1)
        ranges =np.array([tempdf.high-tempdf.low,tempdf.high-tempdf.pre_close,tempdf.pre_close-tempdf.low]) #shape (3,n)
        tempdf['tr'] = pd.DataFrame(ranges).T.abs().max(axis=1)

        #求atr用三种方方法，值是一致的
        # #方法1：使用talib的EMA函数
        # tempdf['atr']=tb.EMA(tempdf.tr,timeperiod)

        # #方法2：计算alpha后用emw函数，并且使用alpha参数
        # #根据跨度衰减
        # alpha = 2.0/(timeperiod+1)
        # tempdf['atr'] =tempdf['tr'].ewm(alpha=alpha,min_periods=timeperiod).mean()

        #方法3，直接用ewm的span参数 （自己会按上面公式计算alpha）
        if type == 'ewm':
            tempdf['atr'] = tempdf['tr'].ewm(span=timeperiod,min_periods=timeperiod).mean() #通过span，根据范围衰减
        else:
            tempdf['atr'] = tempdf['tr'].rolling(window=timeperiod).mean()
        data['atr'] = tempdf['atr']
        return data


    # 平均成交量
    # type:
    # 1:high-low;
    # 2: close-open;
    # 3: alpha(high-low) + (1-alpha)(close-open)
    @staticmethod
    def avevolume(data,avetype=3,alpha=0.5):
        # print(type)
        if avetype==1:
            avevolumes = data['volume']/ (100*(data['high']-data['low']))
        elif avetype==2:
            avevolumes = data['volume'] /(100*np.abs((data['close']-data['open'])))
        elif avetype == 3:
            avevolumes= alpha* (data['volume'] /(100*(data.high-data.low)))+(1-alpha)*(data['volume'] /(100*np.abs(data['close']-data['open'])))
        data['avevolume'] = avevolumes.astype(int)
        return data


    @staticmethod
    #TBD
    def supertrend(data,multiplier=3,timeperiod=14 ):
        tempd = pd.DataFrame(data,columns=['high','low','close'])
        tempd['pre_close']=tempd.close.shift(1)
        tempd['src'] = (data.high+data.low)/2
        tempd = QuantIndex.myatr(tempd,timeperiod)

        #计算上轨
        tempd['dn'] = tempd['src']+multiplier*tempd['atr']
        #计算下轨
        tempd['up'] = tempd['src']-multiplier*tempd['atr']

        tempd['trendup'] = 0.0
        tempd['trenddn'] = 0.0
        tempd['trend'] = 1.0
        tempd['tls'] = 0.0

        tempd = tempd.fillna(0)

        for i in range(len(tempd)):
            tempd['trendup'].values[i] = max(tempd.up.values[i], tempd.trendup.values[i - 1]) if tempd.close.values[
                                                                                                     i - 1] > \
                                                                                                 tempd.trendup.values[
                                                                                                     i - 1] else \
            tempd.up.values[i]

            tempd['trenddn'].values[i] = min(tempd.dn.values[i], tempd.trenddn.values[i - 1]) if tempd.close.values[
                                                                                                     i - 1] < \
                                                                                                 tempd.trenddn.values[
                                                                                                     i - 1] else \
            tempd.dn.values[i]
            tempd['trend'].values[i] = 1 if (tempd['close'].values[i] > tempd['trenddn'].values[i - 1]) else (
                -1 if (tempd['close'].values[i] < tempd['trendup'].values[i - 1]) else tempd['trend'].values[i - 1])

            tempd['tls'].values[i] = tempd['trendup'].values[i] if (tempd['trend'].values[i] == 1) else \
            tempd['trenddn'].values[i]
            # tempd['linecolor'].values[i] = 'Long' if (tempd['Trend'].values[i] == 1) else 'Short'
        # print(tempd)
        data['trendup'] = tempd['trendup']
        data['trenddn'] = tempd['trenddn']
        data['trend'] = tempd['trend']
        return data



    '''
       N表示计算一个coef需要给OLS算法多少天的数据，
       M表示计算多少个coef，并且针对M个coef进行规范化，得出RSRS的值
       '''
    @staticmethod
    def rsrs(data, N=18, M=600):
        # print('===RSRS Index====')
        # print(data.head())
        start = -(N + M - 1)
        highs = data.high.values[start:]
        lows = data.low.values[start:]
        # print(highs)
        # print(lows)
        coefs = np.zeros(shape=(M,))  # 各期斜率
        # print(coefs)
        for i in range(M):
            y = highs[i:i + N]
            x = lows[i:i + N]
            X = sm.add_constant(x)  # (-1,2)
            model = sm.OLS(y, X)
            results = model.fit()
            coefs[i] = results.params[1]  # 预测的线性方程的系数a result.tvalues是b （y=ax+b) 用这个方法算出来的和sklearn的LinearRegression差不多
            # 记录最后一期的Rsquared(可决系数)
            if i == M - 1:
                R_squared = results.rsquared
        # print(coefs)
        # np_coefs = np.array(coefs)
        # 最近期的标准分 归一化
        # z_score = (coefs[-1] - coefs.mean()) / coefs.std()
        z_score = (coefs[-1] - np.mean(coefs))/np.std(coefs,ddof=0)
        # RSRS得分
        rs = z_score * R_squared
        # print(coefs[-1],coefs.mean(),coefs.std())
        return rs, z_score, coefs


    @staticmethod
    def psy(data,P=12,m=6):
        tempdb = pd.DataFrame(data,columns=['close'])
        tempdb['pre_close']=tempdb['close'].shift(1)
        # tempdb['diff'] = tempdb.close-tempdb.pre_close
        tempdb['up'] = tempdb.apply(lambda x: 1 if x['close'] > x['pre_close'] else 0,axis =1)
        tempdb['psy'] = np.round(tempdb['up'].rolling(P).sum() / P,3)
        tempdb['mpsy'] = np.round(tempdb.psy.rolling(m).mean(),3)
        data['psy'] = tempdb['psy']
        data['mpsy'] =tempdb['mpsy']
        return data



    @staticmethod
    #red candle number rate （阳线数量率）
    #P 表示周期，eqlhandle表示当发生开盘价等于收盘价时候，当阳线（1）处理还是当阴线（0）处理
    # 周期P内阳线数量占比： 阳线数量/总数量
    def rcnr(data,P=9,eqlhandle=1):
        data['ocd'] =  data.close-data.open #收盘开盘差
        if eqlhandle ==1:
            data['occ'] = data['ocd'].apply(lambda x: 1 if x>=0 else 0) #1 阳线 0阴线
        else:
            data['occ'] = data['ocd'].apply(lambda x: 1 if x > 0 else 0)  # 1 阳线 0阴线
        data['rcr']= data['occ'].rolling(P).sum()/P #某个时间段阳线占比
        # print(data.head(15))
        return data


    #red candle price rate ( 阳线价格率）
    #周期P内，sum(阳线值)/[sum(阳线)+sum(阴线值)]   阳线值=close-open
    # P 表示周期
    #后续可以优化为考虑最高最低
    @staticmethod
    def rcpr(data,P=9):
        data['ocd'] = data.close - data.open  # 收盘开盘差
        tempdf = pd.DataFrame()
        tempdf['ocd'] = data['ocd']
        tempdf['r'] = data['ocd'].apply(lambda x: 1 if x>=0 else 0) #1 阳线 0阴线
        # tempdf['g'] = data['ocd'].apply(lambda x: 1 if x>=0 else -1) #1 阳线 -1阴线
        tempdf['ocdr'] = tempdf['ocd']*tempdf['r'] # 把是阴线的设为0
        # tempdf['ocd_a'] = tempdf['ocd']*tempdf['g']
        tempdf['ocdr_sum'] = tempdf['ocdr'].rolling(P).sum()
        # tempdf['ocda_sum'] = tempdf['ocd_a'].rolling(P).sum()
        tempdf['ocdall_sum'] = tempdf['ocd'].abs().rolling(P).sum()
        tempdf['rcpr'] = np.round(tempdf['ocdr_sum']/tempdf['ocdall_sum'],3)
        # print(tempdf)
        data['rcpr']= tempdf['rcpr']
        return data

    @staticmethod
    #周期内sum（阳线量）/[sum(阴线量）+sum（阳线量）]
    def rcvr(data, P=9,eqlhandle=1):
        data['ocd'] = data.close - data.open  # 收盘开盘差
        tempdf = pd.DataFrame()
        tempdf['ocd'] = data['ocd']
        if eqlhandle == 1:
            tempdf['r'] = data['ocd'].apply(lambda x: 1 if x >= 0 else 0)  # 1 阳线 0阴线
        else:
            tempdf['r'] = data['ocd'].apply(lambda x: 1 if x > 0 else 0)  # 1 阳线 0阴线
        # tempdf['g'] = data['ocd'].apply(lambda x: 0 if x >= 0 else 1)  # 1 阳线 0阴线
        tempdf['rcv'] = data['volume'] * tempdf['r']
        data['rcvr'] = np.round(tempdf['rcv'].rolling(P).sum()/data['volume'].rolling(P).sum(),3)
        # print(tempdf)
        print(data)
        return data


    '''
    type :
     r 上涨率   r/(r+f)
     f 下跌率:  f/(r+f)
     rf 上涨/下跌
    
    '''
    @staticmethod
    def risefallratio(data,type='r'):
        if type == 'r':
            data['ratio'] = np.round(data.rise_num / (data.fall_num+data.rise_num), 2)
        elif type == 'f':
            data['ratio'] = np.round(data.fall_num / (data.fall_num + data.rise_num), 2)
        else:
             data['ratio'] = np.round(data.rise_num/data.fall_num,2)
        return data

    '''
     阴线阳线比
     type 1: yang /(yin+yang)
     type 2: yin /(yin+yang)
     type 3: yang/yin
     type 4: yin/yang
    '''
    @staticmethod
    def yinyangratio(data,type=1):
        pass

    # TBD
    # 某个交易数据（不然收盘或成交量）的方差，表示某个阶段的波动程度（变量和期望之间）

#TBD
    #两个指标的协方差，表示两个指标之间的偏离程度

