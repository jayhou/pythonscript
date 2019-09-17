import MySQLdb

myDB = MySQLdb.connect(host="hm-data-onedata.cavesgymhprc.rds.cn-north-1.amazonaws.com.cn",port=3306,user="developer",passwd="developer",db="data_analytics_test")
cHandler = myDB.cursor()
cHandler.execute("SHOW DATABASES")
results = cHandler.fetchall()