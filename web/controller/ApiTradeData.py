from flask import Blueprint
from service.StockData import StockData
import pandas as pd
from config.StockConfig import Freq
from config.StockConfig import Echart_OCHL

stock = Blueprint('data',__name__)


#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)

sd = StockData()

@stock.route('/<code>/<market>/<freq>/<startdate>/<enddate>')
def data(code,market,freq,startdate,enddate):

    if freq == "1":
        _freq = Freq.Min_1
    elif freq == '5':
        _freq = Freq.Min_5
    elif freq == '10':
        _freq = Freq.Min_10
    elif freq == '15':
        _freq = Freq.Min_15
    elif freq == '30':
        _freq = Freq.Min_30
    elif freq == '60':
        _freq = Freq.Min_60
    elif freq == 'd':
        _freq = Freq.Day
    elif freq == 'w':
        _freq = Freq.Week
    elif freq == 'm':
        _freq = Freq.Month
    if _freq == Freq.Week or _freq == Freq.Month:
        if market == 'sh':
            _code = 'sh.' + code
        elif market == 'sz':
            _code = 'sz.' + code
        else:
            return "market error"
        df = sd.getLongPeriodData(symbol=_code,freq=_freq,start=startdate,end=enddate,istimeindex=False)
    else:
        if market =='sh':
            _code='SHSE.'+code
        elif market == 'sz':
            _code = 'SZSE.'+code
        else:
            return "market error"
        df = sd.getShortPeriodData(symbol=_code,freq=_freq,start=startdate,end=enddate,istimeindex=False)
    # df['dif'] =  df.apply(lambda x: (1 if (x['close']-x['open'])>=0 else -1),axis=1)
    # df['index'] = df.index.values
    # print(df)
    # print(df.dtypes)
    times = df.time.values.tolist()
    values = df[Echart_OCHL].values.tolist()
    # volumes = df[['index','volume','dif']] .values.tolist()
    volumes = df['volume'].values.tolist()
    # indexes = df.index.values.tolist()

    print(times)
    print(values)
    print(volumes)

    return {"code":code,"times":times,"values":values,"volume":volumes}


