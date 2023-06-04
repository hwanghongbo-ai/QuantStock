# coding=utf-8

from datasource.HbDataSource import HbDataSource
from datasource.JueJingDataSource import JueJingDataSource
from datasource.BaoDataSource import BaoDataSource
from datasource.WormsDataSource import WormsDataSource
from core.Singleton import Singleton


#单例Singleton 模式
@Singleton
class QuantDataSourceManager(object):
    def __init__(self):
        self.juejingdatasource = None
        self.hbdatasource = None
        self.baodatasource = None
        self.wormsdatasource = None


    def jueJingDataSource(self):
        if self.juejingdatasource is None:
            self.juejingdatasource = JueJingDataSource()
        return self.juejingdatasource

    def hbDataSource(self):
        if self.hbdatasource is None:
            self.hbdatasource = HbDataSource()
        return self.hbdatasource

    def baoDataSource(self):
        if self.baodatasource is None:
            self.baodatasource = BaoDataSource()
        return self.baodatasource

    def wormsDataSource(self):
        if self.wormsdatasource is None:
            self.wormsdatasource = WormsDataSource()
        return self.wormsdatasource


