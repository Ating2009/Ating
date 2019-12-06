import pymysql

# 使用 connect 方法，传入数据库地址，账号密码，数据库名就可以得到你的数据库对象
db = pymysql.connect(host="127.0.0.1",port=3306,user= "root",password=
"31415926", database="avidol",charset="utf8")

# 接着我们获取 cursor 来操作我们的 avIdol 这个数据库
cursor = db.cursor()

# 删除一条记录
sql = "delete from beautyGirls where age = '%d'" % (18)
try:
   cursor.execute(sql)
   db.commit()
except:
   db.rollback()