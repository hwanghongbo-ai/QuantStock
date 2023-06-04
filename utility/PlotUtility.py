# coding=utf-8
import matplotlib.pyplot as plt

from render.EchartRender import EchartRender
from service.QuantIndex import QuantIndex
from datasource.JueJingDataSource import TimeColumnName

class PlotUtility(object):
    def __init__(self):
        pass

    @staticmethod
    def ShowPlot(x,ys,labels,colors,xlable,ylable,title):
        plt.figure(figsize=(16, 8))
        for i in range(len(ys)):
            plt.plot(x,ys[i],label=labels[i],c=colors[i])
        plt.xlabel(xlable)
        plt.ylabel(ylable)
        plt.title(title)
        plt.legend()
        plt.show()

    @staticmethod
    def ShowEchart(data):
        render = EchartRender()
        filter = QuantIndex()
        data = filter.macd(data)
        data =  filter.sma(data,[5,10,20])
        ochl = data[['open','close','high','low']]
        vol =  data[['volume']]
        sma = data[['SMA5','SMA10','SMA20']]
        macd = data[['DIF','DEA','HIST']]

        dic = dict()
        dic['ochl'] = ochl
        # dic['close'] = close
        dic['sma'] = sma
        dic['vol'] = vol
        dic['macd'] = macd

        render.setXAxisData(data[TimeColumnName].values.tolist())
        render.showChart(dic)

