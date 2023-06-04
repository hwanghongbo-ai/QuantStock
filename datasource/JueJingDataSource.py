# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import datetime


from config.StockConfig import TimeColumnName
from config.StockConfig import Freq



class JueJingDataSource(object):
    def __init__(self):
        # super(self)
        set_token('05f1014502ff94693272ccd783f2fdd9f33d0c59')


    def getLatestTradeDate(self,exchange='SZSE'):
        current_date =  datetime.datetime.now().date()
        if len(get_trading_dates(exchange=exchange, start_date=current_date, end_date= current_date)) == 0:
            previoustradingdate = get_previous_trading_date(exchange=exchange, date=current_date)
            current_date = datetime.datetime.strptime(previoustradingdate, '%Y-%m-%d')
        return current_date,current_date.strftime('%Y-%m-%d')

    # isdateformat, 返回时间为日期形字符串
    def getData(self,symbol,freq,start,end=None,istimeindex=False,isdateformat=False):
        if end is None:
            # end = get_previous_trading_date(symbol[:4], datetime.now())
            _,end = self.getLatestTradeDate(symbol[:4])

        freq=self.__freq(freq)
        df = history(symbol=symbol, frequency=freq, fields='symbol, open, close, low, high, volume,amount,eob',
                         start_time=start, end_time=end, adjust=ADJUST_PREV, df=True)
        df.rename(columns={'eob':TimeColumnName}, inplace=True)
        if isdateformat:
            df[TimeColumnName] = df[TimeColumnName].dt.strftime('%Y-%m-%d')
            # df[TimeColumnName] = df[TimeColumnName].dt.date

        if istimeindex is True:
             df.set_index(TimeColumnName,inplace=True)

        df = df.round(2)
        return df



    #返回df的索引是time
    # ts = {'hour': 10, 'minute': 30}
    def getDataWithTS(self,symbol,ts,start,end=None):
        # 1. 获取30分数据
        freq= '1800s'
        rd = self.getData(symbol,freq,start,end,istimeindex=False,isdateformat=False)
        hour = ts['hour']
        minute = ts['minute']
        # df = rd[(rd.eob.dt.hour == hour) & (rd.eob.dt.minute == minute)][['close', 'volume', 'eob']]
        # df.eob = df.eob.dt.date
        df = rd[(rd[TimeColumnName].dt.hour == hour) & (rd[TimeColumnName].dt.minute == minute)][['close', 'volume', TimeColumnName]]
        df[TimeColumnName] = df[TimeColumnName].dt.date

        # td_hour = str(hour) + 'h'
        # td_min = str(minute) + 'm'
        # if minute == 0:
        #     df.eob = df.eob - pd.Timedelta(td_hour)  # '10h')  # 减去10小时
        # else:
        #     df.eob = df.eob - pd.Timedelta(td_hour) - pd.Timedelta(td_min)  # '10h')  # 减去10小时
        # # df.rename(columns={'close': 'close_ts', 'volume': 'volume_ts','eob':'time'}, inplace=True)

        # df.rename(columns={'eob': TimeColumnName}, inplace=True)
        df.set_index(TimeColumnName, inplace=True)

        # print(df)
        #
        # #2. 获取日K数据
        data = self.getData(symbol,'1d',start,end,istimeindex=True,isdateformat=True)
        # print(data)
        # print(df.shape,data.shape)

        # # 3.合并
        # data[['close_ts', 'volume_ts']] = df[['close_ts',  'volume_ts']]
        data[['close_ts', 'volume_ts']] = df[['close', 'volume']]
        #
        # print(data)
        # print(df.shape, data.shape)

        return data


    # 获取所有ETF
    def getetfs(self):
        sectype = SEC_TYPE_FUND
        df = get_instruments(sec_types=sectype, df=True, fields="symbol,exchange,sec_id,sec_name",
                             exchanges='SHSE, SZSE')
        print(df)
        return df

    # 获取所有指数
    def getindexes(self):
        sectype = SEC_TYPE_INDEX
        df = get_instruments(sec_types=sectype, df=True, fields="symbol,exchange,sec_id,sec_name",
                             exchanges='SHSE, SZSE')

        print(df)
        return df

    """
       获取当日A股代码（剔除次新股，退市股和非上市股）
       :exchanges: 多个交易所代码可用 ,(英文逗号)分割, 也支持 ['exchange1', 'exchange2'] , 默认 None 表示所有
       :param new_days:新股上市天数，默认为365天
   """
    def get_normal_stocks(self, exchanges=None,skip_list_days=365):
        date = datetime.date.today()
        # 先剔除退市股、次新股和B股
        # df_code = get_instrumentinfos(sec_types=SEC_TYPE_STOCK, exchanges=exchanges,fields='symbol, sec_name,listed_date, delisted_date', df=True)
        df_code = get_instruments(symbols=None,exchanges=exchanges, sec_types=SEC_TYPE_STOCK, skip_suspended = True,skip_st=False,fields='symbol, sec_name,listed_date,delisted_date,trade_date',df=True)
        # df_code['listed_date'] = df_code['listed_date'].apply(lambda x: x.replace(tzinfo=None))
        # df_code['delisted_date'] = df_code['delisted_date'].apply(lambda x: x.replace(tzinfo=None))
        df_code['listed_date'] = df_code.listed_date.dt.date
        df_code['delisted_date'] = df_code.delisted_date.dt.date
        df_code['trade_date'] = df_code.trade_date.dt.date
        df_code = df_code[df_code.trade_date == date]
        # print(df_code)
        if skip_list_days == 0:
        #     all_stocks = [code for code in df_code.symbol.to_list() if code[:6] != 'SHSE.9' and code[:6] != 'SZSE.2']
            all_stocks = [code for code in df_code.symbol.to_list()]
        else:
            listeddate = (date - datetime.timedelta(days=skip_list_days))
            # print(date, type(date),listeddate,type(listeddate))
            # print(df_code.dtypes)
            # print(df_code[df_code.listed_date <= listeddate])
            all_stocks = [code for code in df_code[(df_code['listed_date'] <= listeddate)].symbol.to_list()]
        #     all_stocks = [code for code in df_code[(df_code['listed_date'] <= date - datetime.timedelta(days=new_days)) & (
        #         df_code['delisted_date'] > date)].symbol.to_list() if code[:6] != 'SHSE.9' and code[:6] != 'SZSE.2']
        all_stocks_str = ','.join(all_stocks)
        return all_stocks, all_stocks_str

    '''
    获取标的的当日最高最低价
    '''
    def getUpperLowlimitPrice(self,symbols):
        df = get_instruments(symbols=symbols,exchanges=None, sec_types=SEC_TYPE_STOCK, skip_suspended = True, skip_st=False,
                             fields='symbol, sec_name,trade_date,pre_close,upper_limit,lower_limit',df=True)
        return df




    '''
    获取基本面信息
    '''
    def getFundaments(self,symbols,fields,start_date, end_date):
        if end_date is None:
            # end_date = get_previous_trading_date(symbols[:4], datetime.now())
            _,end_date= self.getLatestTradeDate(symbols[:4])

        for field in fields:
            table = self.__table4field(field)
            if table is None:
                continue
            get_fundamentals(table=table,symbols=symbols,)
        df = get_fundamentals(table='deriv_finance_indicator', symbols=symbols, start_date=start_date, end_date=end_date,
                         fields='ACCRECGTURNDAYS,ACCRECGTURNRT,ASSLIABRT,OPGPMARGIN,SGPMARGIN', df=True)
        return df
    '''
    balance_sheet:
        ACCORECE:应收账款  ACCOPAYA:应付账款	ADVAPAYM:预收款项	 GOODWILL:商誉	
        
    income_statement:
        'BASICEPS',基本每股收益	 'BIZTOTINCO',营业总收入	 'MAINBIZINCO',主营业务收入	'NETPROFIT',净利润	
        'PERPROFIT',营业利润	 'TOTPROFIT',利润总额	
        
    prim_finance_indicator:
        'EPSBASIC',基本每股收益  'EPSBASICEPSCUT',扣除非经常性损益后的基本每股收益	 
        'EPSFULLDILUTED',稀释每股收益 'EPSFULLDILUTEDCUT',扣除非经常性损益后的稀释每股收益	
        'OPNCFPS',每股经营活动产生的现金流量净额	 'ROEWEIGHTED',净资产收益率_加权	
    
     deriv_finance_indicator:
        ACCRECGTURNDAYS:应收账款周转天数  ACCRECGTURNRT:应收账款周转率	ASSLIABRT:资产负债率
        OPGPMARGIN:营业毛利润	 SGPMARGIN:销售毛利率	
    '''

    def __table4field(self,field):
        balance_sheet = ['ACCORECE','ACCOPAYA','ADVAPAYM','GOODWILL']
        income_statement=['BASICEPS','BIZTOTINCO','MAINBIZINCO','NETPROFIT','PERPROFIT','TOTPROFIT']
        prim_finance_indicator = ['EPSBASIC','EPSBASICEPSCUT','EPSFULLDILUTED','EPSFULLDILUTEDCUT','OPNCFPS','ROEWEIGHTED']
        deriv_finance_indicator=['ACCRECGTURNDAYS' ,'ACCRECGTURNRT','ASSLIABRT','OPGPMARGIN','SGPMARGIN']
        table = None
        if field in balance_sheet:
            table = 'balance_sheet'
        elif field in income_statement:
            table = 'income_statement'
        elif field in prim_finance_indicator:
            table = 'prim_finance_indicator'
        elif field in deriv_finance_indicator:
            table = 'deriv_finance_indicator'
        return table

    def __freq(self, klinetype):

        if klinetype == Freq.Min_1:
            freq = '60s'
        elif klinetype == Freq.Min_5:
            freq = '300s'
        elif klinetype == Freq.Min_10:
            freq = '600s'
        elif klinetype == Freq.Min_15:
            freq = '900s'
        elif klinetype == Freq.Min_30:
            freq = '1800s'
        elif klinetype == Freq.Min_60:
            freq = '3600s'
        elif klinetype == Freq.Day:
            freq = '1d'
        elif klinetype == Freq.Week:
            freq = '1d'
        elif klinetype == Freq.Month:
            freq = '1d'
        elif klinetype == Freq.Year:
            freq = '1d'
        else:
            freq = klinetype
        return freq