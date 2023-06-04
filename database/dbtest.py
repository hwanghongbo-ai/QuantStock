from DBHelper import MySQLHelper
import pandas as pd

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)


if __name__ == '__main__':
    db = MySQLHelper()
    sql = "select * from beixiang limit 10"
    df = db.selectbypd(sqlstr=sql)
    print(df)
    del db