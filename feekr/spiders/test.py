# import pymysql
#
# connect = pymysql.connect(
#             host="127.0.0.1",
#             port=3306,
#             db="ivantest",
#             user="root",
#             passwd="a12345678",
#             charset='utf8',
#             use_unicode=True
#         )
# cursor = connect.cursor(pymysql.cursors.DictCursor)
#
# sql = """insert into `aritcal` (`artical_title`,`user_id`,``)
#                 value (%s)""",
#         ('','')
#         self.cursor.execute(sql)
# cursor.execute("select `user_id` from user where `user_name` = %s", ('沈222氏蘑菇汤'))
# userid = cursor.fetchone()
# if userid:
#     print(userid['user_id'])
# else:
#     print(userid)
# import random
# print(random.randint(10, 100))
