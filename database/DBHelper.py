# coding=utf-8

# mysql连接基本库

import pymysql as mysql

# 读取配置文件所需要的库
import configparser
import os

# 线程管理所需要的库
import threading
import queue
from core.Singleton import SingletonMetaClass
from core.Singleton import Singleton
import pandas as pd


# 创建数据库配置配置文件
class Config(object):
    def __init__(self, configFileName='db.cnf'):
        file = os.path.join(os.path.dirname(__file__), configFileName)
        self.config = configparser.ConfigParser()
        self.config.read(file)

    def getSections(self):
        return self.config.sections()

    def getOptions(self, section):
        return self.config.options(section)

    def getContent(self, section):
        result = {}
        for option in self.getOptions(section):
            value = self.config.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


# 将连接所需要的参数封装在对象中
# 依次为: 数据库密码、需要连接的库名、主机地址[默认 localhost]、端口号[默认 3306]、初始化连接数[默认 3]、最大连接数[默认 6]
class parameter(object):
    def __init__(self, password, database, host="localhost", port="3306",user = "root", initsize = 3, maxsize = 6):
        self.host = str(host)
        self.port = int(port)
        self.user = str(user)
        self.password = str(password)
        self.database = str(database)
        self.maxsize = int(maxsize)
        self.initsize = int(initsize)


# 连接池
# class DBConnPool(parameter,metaclass=SingletonMetaClass):
class DBConnPool(parameter):
    def __init__(self, fileName='db.cnf', configName='mysql'):
        # 加载配置文件, 配置文件名默认为 'db.cnf', 配置标签默认为 'mysql'
        self.config = Config(fileName).getContent(configName)
        super(DBConnPool, self).__init__(**self.config)
        # 创建队列作为 池
        self.pool = queue.Queue(maxsize=self.maxsize)
        self.idleSize = self.initsize
        # 创建线程锁
        self._lock = threading.Lock()
        # 初始化连接池
        for i in range(self.initsize):
            # 创建 初始化连接数 数量的连接放入池中
            self.pool.put(self.__createConn())
        # 启动日志
        print('\n')
        print('\033[1;32m DBConnPool connect database {database}, login is {user} \033[0m'.format(database=self.database, user=self.user))

    # 生产连接
    def __createConn(self):
        # 使用mysql基本类
        try:
            conn= mysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.password,
                               database=self.database,
                               charset='utf8')

        except Exception as e:
            print("connect failed with reason {}".format(e))
            conn = None
        # print('--connect db {} , {} , {} ,{} ,{}, result is {}'.format(self.host, self.port, self.user, self.password, self.database,result))
        return conn

    # 获取连接
    def getConn(self):
        self._lock.acquire()
        try:
            # 如果池中连接够直接获取
            if not self.pool.empty():
                self.idleSize -= 1
            else:
                # 否则重新添加新连接
                if self.idleSize < self.maxsize:
                    self.idleSize += 1
                    self.pool.put(self.__createConn())
        finally:
            self._lock.release()
            return self.pool.get()

    # 释放连接
    def releaseCon(self, conn=None):
        try:
            self._lock.acquire()
            conn.cursor().close()   #hhb
            # 如果池中大于初始值就将多余关闭，否则重新放入池中
            if self.pool.qsize() < self.initsize:
                self.pool.put(conn)
                self.idleSize += 1
            else:
                try:
                    # 取出多余连接并关闭
                    surplus = self.pool.get()
                    surplus.close()
                    del surplus
                    self.idleSize -= 1
                except mysql.ProgrammingError as e:
                    raise e
        finally:
            self._lock.release()

    def clearPool(self):
        try:
            while True:
                conn = self.pool.get_nowait()
                if conn:
                    conn.close()
        except queue.Empty:
            pass


        # 释放连接池本身
    def __del__(self):
        self.clearPool()


 #单例Singleton 模式
@Singleton
class MySQLHelper(object):

    def __init__(self):
        self.pool = DBConnPool()

#  单例无法被调用del
    def __del__(self):
        print('delete {} '.format(self.__class__))
        # del self.pool
        self.destroy()


    def destroy(self):
        self.pool.clearPool()


   #返回双重数组
    def select(self,sqlstr):
        try:
            conn = self.pool.getConn()
            cursor = conn.cursor()
            cursor.execute(sqlstr)
            records = cursor.fetchall()
        except Exception as e:
            records=()
            print(e)
        finally:
            self.pool.releaseCon(conn)
        return records

    def selectbypd(self,sqlstr):
        conn = self.pool.getConn()
        try:
            return pd.read_sql(sql=sqlstr,con=conn)
        except Exception as e:
            print(e)
        finally:
            self.pool.releaseCon(conn)



   # sample:
   # db.insert("Person", keys=['name', 'age', 'sex', 'income'], values=["\'lxy\'", 46, "\'f\'", 10000])
    def insert(self,table,keys,values):
        sqlstr = "insert into {}(".format(table)
        for key in keys:
            sqlstr = (sqlstr + "{},").format(key)
        sqlstr = sqlstr[:-1]+') values('
        for value in values:
            sqlstr = (sqlstr + "{},").format(value)
        sqlstr = sqlstr[:-1] + ")"
        print(sqlstr)
        return self.excute(sqlstr,True)


    # Sample:
    # db.createTable("Person", ["id", "name", "age", "sex", "income"],
    #               types=["INT", "varchar(20)", "INT", "varchar(2)", "FLOAT"],
    #                nulls=['NOT NULL', '', '', '', ''],
    #               indexes=[True,False,False,False,False],defualts=['auto_increment','','','',''])

    def createTable(self,table,keys,types,indexes,nulls,defualts):
        sqlstr = "create table {} (".format(table)
        for i in range(len(keys)):
            if indexes[i]:
                sqlstr= sqlstr +"{} {} primary key {} {},".format(keys[i],types[i],nulls[i],defualts[i])
            else:
                sqlstr = sqlstr + "{} {} {} {},".format(keys[i], types[i], nulls[i],defualts[i])
        sqlstr = sqlstr[:-1]+")"
        print(sqlstr)
        return self.excute(sqlstr,True)


    def excute(self,sqlstr,istransaction=True):
        result = True
        try:
            conn = self.pool.getConn()
            conn.cursor().execute(sqlstr)
            if istransaction:
                conn.commit()
        except Exception as e:
            result = False
            print(e)
            if istransaction:
                conn.rollback()
        finally:
            self.pool.releaseCon(conn)
        return result

    def getTableColums(self,table):
        sql = r"select COL.COLUMN_NAME FROM	INFORMATION_SCHEMA.COLUMNS COL WHERE COL.TABLE_NAME = '{}'".format(table)
        fields =  self.select(sqlstr=sql)
        flist = [ field[0] for field in fields]
        return flist












