# coding=utf-8
import pandas as pd
import datetime
import json
import numpy as np


class PDTools(object):
    def __init__(self):
        pass

    ''''
    #把df1，df2 merge,并把不同的index去掉
    '''
    @staticmethod
    def DropDifferentIndex(df1,df2):
        df = pd.merge(df1, df2, how='inner', left_index=True, right_index=True)
        dfx = pd.DataFrame()
        dfy = pd.DataFrame()
        c1 = list(df1) #获取原始列名
        # c2 = list(df2)
        for c in c1:
            dfx[c]=df[c+'_x']
            dfy[c] = df[c+'_y']
        # print(c1,c2)
        # print(df.tail(5))
        # print(dfx.tail(5))
        # print(dfy.tail(5))
        # print(df.shape,dfx.shape,dfy.shape)
        return dfx,dfy

    '''
    给定日期，获得该日前或后几日的日期
    '''
    @staticmethod
    def DateAfterOrBeforeSomePeriods(datestr,periods,isbefore):
        _date = datetime.datetime.strptime(datestr,'%Y-%m-%d')
        _periods = datetime.timedelta(days=periods)
        if isbefore:
            _date = _date-_periods
        else:
            _date = _date+_periods
        return _date.strftime('%Y-%m-%d')

    @staticmethod
    def FilterDatasAfterPeriods(source,anchors,periods):
        # print(source)
        # print(anchors)
        len = anchors.shape[0]
        dic=dict()
        for targetday in periods:
            tdv = pd.DataFrame()
            for item in range(len):
                index = anchors.iloc[[item]].index.tolist()[0]
                ix = PDTools.Index2Row(source,index)
                ix = ix + targetday
                tdv = tdv.append(source.iloc[[ix]])
            dic["target_{}".format(targetday)] = tdv
        return dic


    @staticmethod
    def Index2Row(data,index):
        data1 = data.loc[:index]
        return data1.shape[0]-1


    @staticmethod
    # orient: None, index,  record, values, table
    def toJson(df,orient=None):
        jsonstr = df.to_json(orient=orient) #基本使用record,index,values,table比较好
        return json.loads(jsonstr),jsonstr

    #json按列显示
    @staticmethod
    def toJsonbyColumn(df):
        dic = dict()
        # col = df.columns.values
        for column in df:
            dic[column] = df[column].values.tolist()
        return json.dumps(dic)


    @staticmethod
    #### 2. 中位数去极值函数 ####################################################
    def winsorize(df, factor, n=20):
        '''
        df为bar_dictFrame数据
        factor为需要去极值的列名称
        n 为判断极值上下边界的常数
        '''
        ls_raw = np.array(df[factor].values)
        ls_raw.sort(axis=0)
        # 获取中位数
        D_M = np.median(ls_raw)

        # 计算离差值
        ls_deviation = abs(ls_raw - D_M)
        ls_deviation.sort(axis=0)
        # 获取离差中位数
        D_MAD = np.median(ls_deviation)

        # 将大于中位数n倍离差中位数的值赋为NaN
        df.loc[df[factor] >= D_M + n * D_MAD, factor] = None
        # 将小于中位数n倍离差中位数的值赋为NaN
        df.loc[df[factor] <= D_M - n * D_MAD, factor] = None

        return df



