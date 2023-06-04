# coding=utf-8
import numpy as np
import statsmodels.api as sm
import pandas as pd

pd.set_option('display.float_format', lambda x: '%.3f' % x)

"""
 本类的目的是获取指定时间段内K线数据的一些特征，比如macd交叉，macd金叉，均线梯度等
"""

class QuantFilter(object):
    def __init__(self):
        pass

    # 百分数预处理，返回当日open，close，某个时间点，成交量相对于前收盘或前成交量的涨跌幅百分数
    def pct(self,data,fileds,dropnan=True):
        tempd = pd.DataFrame(data,columns=['open','close','close_ts','volume'])
        tempd['preclose'] = tempd['close'].shift(1)
        tempd['prevolume'] = tempd['volume'].shift(1)
        # print(tempd.tail(10))
        rp = 3
        if 'close' in fileds:
            data['close_pct'] = np.round(tempd['close'] / tempd['preclose'] - 1, rp) * 100
        if 'open' in fileds:
            data['open_pct'] = np.round(tempd['open'] / tempd['preclose'] - 1, rp) * 100
        if 'close_ts' in fileds:
            data['ts_pct'] = np.round(tempd['close_ts'] / tempd['preclose'] - 1, rp) * 100
        if 'volume' in fileds:
            data['vol_pct'] = np.round(tempd['volume'] / tempd['prevolume'] -1, rp)*100
        if dropnan:
            data = data[1:]
        return data

    #fields ： 列表，['upshadow','upshadow','entity']或者其中一个，二个，三个的组合列表，
    # ispct： true表示转化成百分比（和前一个收盘价比），false表示绝对数值
    def candleanalyse(self,data,fields,ispct=True):
        # tempd = pd.DataFrame(data, columns=['open', 'close', 'high', 'low'])
        if 'upshadow' in fields:
            data['upshadow'] = data.apply(lambda x: (x['high']-x['close']) if x['close']>x['open'] else (x['high']-x['open']),axis=1)
            if ispct:
                data['upshadow'] = np.round(data['upshadow'] / data['close'].shift(1),4)*100

        if 'downshadow' in fields:
            data['downshadow'] = data.apply(lambda x: (x['open'] - x['low']) if x['close'] > x['open'] else (x['close'] - x['low']),axis=1)
            if ispct:
                data['downshadow'] = np.round(data['downshadow'] / data['close'].shift(1) , 4) * 100

        if 'entity' in fields:
            data['entity'] = data['close']-data['open']
            if ispct:
                data['entity'] = np.round(data['entity'] / data['close'].shift(1) , 4) * 100

        return data



    #计算所给数据的梯度
    def gradient(self,data):
        trian_x = np.arange(data.shape[0])
        train_y =data
        cx = sm.add_constant(trian_x)  # 把shape(n,) reshape为(n,2)
        # cx = np.reshape(x_train,(-1,1))
        model = sm.OLS(train_y, cx)
        result = model.fit()
        return (round(result.params[1], 3))


    # 阳线实体反包，
    # 前一根阴线，后一根阳线反包
    # open[0] < close[-1] & close[0] > open[-1] & close[-1]-open[-1] < entity <0)

    def yangxianfanbao(self,data,entity=-3):
        data = self.candleanalyse(data,fields=['entity'],ispct=True)
        data = data[(data['entity'].shift(1) <= entity) & (data['open'] <= data['close'].shift(1)) & (data['close'] >= data['open'].shift(1))]
        # print(data)
        return data

    # 阴线实体反包，
    # 前一根阳线，后一根 阴线反包
    # （open[0] > close[-1] & close[0] < open[-1] & close[-1]-open[-1] > entity > 0 )

    def yingxianfanbao(self, data, entity=3):
        data = self.candleanalyse(data, fields=['entity'], ispct=True)
        data = data[(data['entity'].shift(1) >= entity) & (data['open'] >= data['close'].shift(1)) & (
                    data['close'] <= data['open'].shift(1))]
        # print(data)
        return data




#周期数据（收盘，开盘或者均线）的梯度，这是对多个数据形成的梯度
    def gradients(self,npdata,period):
        gradients = []
        deltas = []
        len = npdata.shape[0]
        trian_x = np.arange(period)
        # print(trian_x)
        for i in range(len-period):
            print('----No.:',i)
            if i== 0 :
                train_y = np.round((npdata[-period:]),2)
            else:
                train_y =np.round((npdata[-period-i:-i]),2)
            delta = np.round((train_y[-1]-train_y[0]),3)
            print('trained data:',train_y,delta)
            cx = sm.add_constant(trian_x)  # 把shape(n,) reshape为(n,2)
            # cx = np.reshape(x_train,(-1,1))
            model = sm.OLS(train_y, cx)
            result = model.fit()
            gradients.append(round(result.params[1],3))
            # deltas.append( round(delta/5.0,3))
            deltas.append(round(delta , 3))
            # print(round(result.params[1],3))
        # print((gradients))
        # print(deltas)
        return gradients[::-1],deltas[::-1]   #反序，原本是时间倒序，最新的在第一个，现在返回顺序，最新的是最后

#一个周期内最大收盘，开盘，最高，最低价
    def maxOCHLsInPeriods(self,data,period=10):
         data['max_close'] = data.close.rolling(period).max()
         data['max_high'] = data.high.rolling(period).max()
         data['max_low'] = data.low.rolling(period).max()
         data['max_open']=data.open.rolling(period).max()
         return data

    # 一个周期内最小收盘，开盘，最高，最低价
    def lowOCHLsInPeriods(self,data,period=10):
         data['min_close'] = data.close.rolling(period).min()
         data['min_high'] = data.high.rolling(period).min()
         data['min_low'] = data.low.rolling(period).min()
         data['min_open'] = data.open.rolling(period).min()
         return data

# 获取某段时间内macd的cross（死叉或者金叉点）
    #返回macd['cross'], 如果1表示金叉点，如果-1表示死叉点
    def macdcross(self, macddate):
        temppd = pd.DataFrame(macddate, columns=['time', 'DIF', 'DEA', 'HIST', 'close'])
        temppd['d1'] = temppd.apply(lambda x: 1 if x['HIST'] > 0 else 0, axis=1)
        # temppd['d2']= (temppd['d1']-temppd['d1'].shift(1)).abs()
        temppd['d2'] = (temppd['d1'] - temppd['d1'].shift(1))
        macddate['cross'] = temppd['d2']
        # dd = data2[data2['cross']!=0]
        # print(data2)
        return macddate

    #获取macd金叉，同时提供有效性分析

    #isdifgrow: 是否排除dif趋势非向上的金叉
    #isdeagrow: 是否排除dea趋势非向上的金叉
    #trendhalfperiod: 判断趋势的周期，2*trendhalfperiod+1,中心点为金叉那个点
    #macdthreshold: 金叉前，macd必须在该值以上，如果金叉前macd低于它，则排除，比如设置0，表示在水面上金叉才有效
    #pthreshold: 金叉到下个死叉（一个周期）需要大于多少天，小于该天排除，作为假金叉 --》 时间扰动排除
    #vthreshold: 一个周期内，最大的macd必须大于该值，小于则该周期为假金叉 --》 幅度扰动排除
    def macdgoldencross(self, macddata,isdifgrow, isdeagrow,trendhalfperiod=3,macdthreshold=None, pthreshold=5, vthreshold=0.12):
        data = self.macdcross(macddata)
        data.dropna(axis=0, how='any', inplace=True)
        # print(data[data.cross != 0])
        data = self.__macdcrossDataClean(data,type=1,pthreshold=pthreshold,vthreshold=vthreshold)
        # print(data[data.cross != 0])

        if macdthreshold != None:
            data = self.__macdgoldencrossabovedifthreshold(data,macdthreshold)
            # print(data[data.cross != 0])

        #根据上升趋势删选
        if isdifgrow and not isdeagrow:
            data = self.__macdgoldencrosswithuptrend('dif',data,trendhalfperiod)

        if isdeagrow and not isdifgrow:
            data = self.__macdgoldencrosswithuptrend('dea',data,trendhalfperiod)

        if isdifgrow and isdeagrow:
            data =self.__macdgoldencrosswithuptrend('all',data,trendhalfperiod)

        # print(data[data.cross != 0])
        return data,data[data.cross !=0]

#  dif, dea 趋势
    # 在指定的点index为中心点，分别取其左右halfperiod ，获得halfperiod+1这个周期内dif,dea的线性回归斜率
    def macddifdeatrend(self,macddata,index,halfperiod):
        if macddata.shape[0] < (index+halfperiod+1):
            return None

        npdifs = macddata.loc[index-halfperiod:index+halfperiod].DIF.values
        npdeas = macddata.loc[index-halfperiod:index+halfperiod].DEA.values
        print(npdifs)
        print(npdeas)
        dif_g= self.gradient(npdifs)
        dea_g = self.gradient(npdeas)
        print(dif_g)
        print(dea_g)
        return dif_g,dea_g



    def rankvol(self,data,period):
        # aa = data['volume'].rolling(period).apply(lambda x: self.handle(x))
        def volrankhandle(x): # 嵌套函数
            return x.rank()[-1:]

        rank = data['volume'].rolling(period).apply(volrankhandle)
        # print(type(aa),aa)

        normedrank = (2*rank-period-1)/(period-1)
            # print(aa)
        return rank,normedrank



    def __macdgoldencrosswithuptrend(self,type,macddata,halfperiod):
        crossed = macddata[macddata.cross != 0.0]
        indexes = crossed.index.values
        removedindexes = []
        for idx in range(indexes.shape[0]-1):  #-1表示不考虑最后一个
            curindex = indexes[idx]
            if crossed.loc[curindex].cross != 1.0:
                continue
            nextindex = indexes[idx + 1]
            dif_g, dea_g = self.macddifdeatrend(macddata, curindex, halfperiod)
            print("trend check ",curindex,dif_g,dea_g)
            if type =='dif' or type=='all':
                if dif_g < 0 :
                    if curindex not in removedindexes:
                        removedindexes.append(curindex)
                    if nextindex not in removedindexes:
                        removedindexes.append(nextindex)
            if type=='dea' or type=='all':
                if dea_g < 0 :
                    if curindex not in removedindexes:
                        removedindexes.append(curindex)
                    if nextindex not in removedindexes:
                        removedindexes.append(nextindex)

        for idx in removedindexes:
            macddata.loc[idx, 'cross'] = 0.0
            print('remove index by trend',idx)

        return macddata

    def __macdgoldencrossabovedifthreshold(self,macddata,difthreshold):
        crossed = macddata[macddata.cross != 0.0]
        indexes = crossed.index.values
        removedindexes =[]
        for idx in range(indexes.shape[0]-1): #-1表示不考虑最后一个
            curindex = indexes[idx]
            if crossed.loc[curindex].cross != 1.0:
                continue
            preindex = indexes[idx] - 1
            nextindex = indexes[idx + 1]

            #金叉方向
            if macddata.loc[preindex].DIF < difthreshold:
                print('不满足DIF条件',curindex,nextindex)
                removedindexes.append(curindex)
                removedindexes.append(nextindex)

        # npremovedindexes = np.array(removedindexes)
        for idx in removedindexes:
            print('remove index by dif threshold ',idx)
            macddata.loc[idx,'cross'] = 0.0

        return macddata

#macd金叉死叉数据清理,排除周期太短或者周期内macd太小
    #type = 1 金叉 type = -1 死叉
    def __macdcrossDataClean(self,macddata,type,pthreshold, vthreshold):
        crossdata = macddata[macddata.cross != 0]
        idxes = crossdata.index.values
        len = idxes.shape[0]
        removeindex = []

        for idx in range(len):
            if idx >= len - 1:
                break
            # print(dd.loc[idxes[idx]])
            if type == 1 and crossdata.loc[idxes[idx]].cross != 1.0:
                continue
            elif type == -1 and crossdata.loc[idxes[idx]].cross != -1.0:
                continue
            # if crossdata.loc[idxes[idx]].cross == 1.0:
            #检查时间是否满足条件
            curindex = idxes[idx]
            nextindex = idxes[idx + 1]
            # print(gx.time,dx.time,type(gx.time-dx.time),(gx.time-dx.time),(gx.time-dx.time).days)
            # 检查金叉到下一个死叉的周期是否过小
            # print('检查时间')
            if (crossdata.loc[nextindex].time - crossdata.loc[curindex].time).days <= pthreshold:
                print('不满足时间', curindex, nextindex)
                removeindex.append(curindex)
                removeindex.append(nextindex)
                continue

            # 判断金叉到下一个死叉之间最大macd是否太小,根据macd value清洗数据
            tmp = macddata.loc[curindex:nextindex]
            # print( (tmp.HIST),tmp['HIST'].max())
            if (tmp.HIST.max() <= vthreshold and type == 1) or (tmp.HIST.min() >= vthreshold and type == -1):
                print('不满足macd条件', curindex, nextindex)
                removeindex.append(curindex)
                removeindex.append(nextindex)

        #排除所有不符合标准的记录
        npremoveindex = np.array(removeindex)
        if npremoveindex.shape[0] > 0:
            for i in range(npremoveindex.shape[0]):
                macddata.loc[removeindex[i], 'cross'] = 0.0

        return macddata













