# import pymysql
#
# # 打开数据库连接
# db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901', database='study', charset='utf8', port=3306)
# # 使用cursor方法获取操作游标
# cursor = db.cursor()
# # 关闭光标对象
# cursor.close()
# # 关闭数据库链接
# db.close()
# print("连接成功！")

#
# import pymysql
#
# # 打开数据库连接
# db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901', database='study', charset='utf8', port=3306)
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
# # 如果STUDENT表存在，就删除
# cursor.execute(("DROP TABLE IF EXISTS STUDENT"))
# # 定义要执行的SQL语句
# sql = """
#     CREATE TABLE STUDENT(
#         NAME CHAR(20),
#         AGE INT,
#         SEX CHAR(1))
# """
# # 执行SQL语句
# cursor.execute(sql)
# # 提交数据
# db.commit()
# # 关闭光标对象
# cursor.close()
# # 关闭数据库连接
# db.close()
#
# print("CREATE TABLE OK")
#
#


# import pymysql
#
# # 打开数据库连接
# db = pymysql.connect(host='rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com', user='zengxueyuan', passwd='Zqy19990901',
#                      database='study', charset='utf8', port=3306)
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
# # 如果STUDENT表存在，就删除
# cursor.execute(("DROP TABLE IF EXISTS STUDENT"))
# # 定义要执行的SQL语句
# sql = """
#     CREATE TABLE STUDENT (
#         NAME CHAR(20),
#         AGE INT,
#         SEX CHAR(1)
#     )
# """
# # 执行SQL语句
# cursor.execute(sql)
#
# # 定义要执行的插入数据的SQL语句
# insert_sql = "INSERT INTO STUDENT(NAME, AGE, SEX) VALUE (%s, %s, %s)"
# data = [("july", 17, "F"), ("jane", 18, "F"), ("jack", 20, "M")]
# # 执行SQL语句
# cursor.executemany(insert_sql, data)
# # 提交数据
# db.commit()
#
# # 关闭光标对象
# cursor.close()
# # 关闭数据库连接
# db.close()
#
# print("insert ok")


#
# import pymysql
#
# db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
# cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS STUDENT")
#
# sql = """
#     CREATE TABLE STUDENT (
#         NAME CHAR(20),
#         AGE INT,
#         SEX CHAR(1)
#     )
# """
# cursor.execute(sql)
# insert_sql = "INSERT INTO STUDENT(NAME, AGE, SEX) VALUE (%s, %s, %s)"
# data = [("july", 17, "F"), ("jane", 18, "F"), ("jack", 20, "M")]
# cursor.executemany(insert_sql, data)
# db.commit()
#
# # 定义要执行的查询数据的sql语句
# query_sql = "SELECT * FROM STUDENT"
# # 使用execute()方法执行sql语句
# cursor.execute(query_sql)
# # 使用fetchall()获取全部数据
# res = cursor.fetchmany(2)
# # 打印获取的数据
# print(res)
#
# cursor.close()
# db.close()



# import pymysql
#
# db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
# cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS MUSIC")
# sql = """
#     CREATE TABLE MUSIC (
#         COMMENT CHAR(225)
#     )
# """
# cursor.execute(sql)
# db.commit()
# cursor.close()
# db.close()
# print("CREATE TABLE OK")


# from music import get_info
#
# data = get_info()
# print(data)



# import pymysql
# from music import get_info
#
# db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
# cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS MUSIC")
# sql = """
#     CREATE TABLE MUSIC (
#         COMMENT CHAR(225)
#     )
# """
# cursor.execute(sql)
# print("CREATE TABLE OK")
#
# # INSERT
# insert_sql = "INSERT INTO MUSIC(COMMENT) VALUES (%s)"
# data = get_info()
# cursor.executemany(insert_sql, data)
# db.commit()
#
# cursor.close()
# db.close()
# print("insert ok")



import pymysql
from music import get_info

db = pymysql.connect(host="rm-uf65wv8008560z9k1co.mysql.rds.aliyuncs.com", user="zengxueyuan", passwd="Zqy19990901", database="study", charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS MUSIC")

sql = """
    CREATE TABLE MUSIC (
        COMMENT CHAR(255)
    )
"""
cursor.execute(sql)
insert_sql = "INSERT INTO MUSIC (COMMENT) VALUES (%s)"
data = get_info()
cursor.executemany(insert_sql, data)
db.commit()

query_sql = "SELECT * FROM MUSIC"
cursor.execute(query_sql)
res = cursor.fetchall()
print(res)

cursor.close()
db.close()
