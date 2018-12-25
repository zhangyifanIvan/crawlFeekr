# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import random


class FeekrPipeline(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            db="ivantest",
            user="root",
            passwd="a12345678",
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor);

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # sql = "SELECT * FROM `user`"
        # self.cursor.execute(sql)
        # result = self.cursor.fetchall()
        # for row in result:
        #     index = row["user_name"]
        #     print(index)
        # print('======================================')
        # print(" address = " + item['address'])
        # print('======================================')
        # self.cursor.execute("""insert into `address` (`address_desc`)
        #                 value (%s)""", item['address'])
        # self.connect.commit()
        self.addressid = self.insert_address(itemvalue=item)
        self.userid = self.insert_user(itemvalue=item)
        self.articalid = self.insert_artical(itemvalue=item)
        self.insert_pics(itemvalue=item)
        self.insert_passages(itemvalue=item)

        return item

    def close_spider(self, spider):
        return

    def insert_user(self, itemvalue):
        userid = self.get_user_id(itemvalue['userName'])
        if userid < 0:
            self.cursor.execute("""insert into `user` (`user_name`,`user_head_img`)
                value (%s,%s)""", (itemvalue['userName'], itemvalue['userImg']))
            self.connect.commit()
            userid = self.get_user_id(itemvalue['userName'])
            return userid
        else:
            return userid

    def get_user_id(self, username):
        self.cursor.execute("select `user_id` from user where `user_name` = %s", (username))
        userid = self.cursor.fetchone()
        if userid:
            return userid['user_id']
        else:
            return -1

    def insert_artical(self, itemvalue):
        aritcalid = self.get_artical_id(title=itemvalue['title'])
        if aritcalid < 0:
            self.cursor.execute(
                """insert into `artical` (`artical_title`, `user_id`, `address_id`, `artical_favor`, `artical_read`) value (%s,%s,%s,%s,%s)""",
                (itemvalue['title'], str(self.userid), str(self.addressid), str(random.randint(10, 100)),
                 str(random.randint(10, 100))))
            self.connect.commit()
            return self.get_artical_id(title=itemvalue['title'])
        else:
            return aritcalid

    def get_artical_id(self, title):
        self.cursor.execute("select `artical_id` from artical where `artical_title` = %s and `user_id` = %s",
                            (title, self.userid))
        name = self.cursor.fetchone()
        if name:
            return name['artical_id']
        else:
            return -1

    def insert_pics(self, itemvalue):
        imagemap = itemvalue['imageMap']
        if imagemap:
            for item in imagemap.items():
                self.cursor.execute(
                    """insert into `artical_pic` (`pic_url`, `artical_id`, `pic_desc`) value (%s,%s,%s)""",
                    (item[0], str(self.articalid), item[1]))
                self.connect.commit()

    def insert_passages(self, itemvalue):
        list = itemvalue['passageList']
        if list:
            for item in list:
                self.cursor.execute(
                    """insert into `artical_passage` (`passage_content`, `artical_id`) value (%s,%s)""",
                    (item, str(self.articalid)))
                self.connect.commit()

    def insert_address(self, itemvalue):
        addressid = self.get_address_id(addressname=itemvalue['address'])
        if addressid < 0:
            self.cursor.execute("""insert into `address` (`address_desc`) value (%s)""", (itemvalue['address']))
            self.connect.commit()
            addressid = self.get_address_id(addressname=itemvalue['address'])
            return addressid
        else:
            return addressid

    def get_address_id(self, addressname):
        self.cursor.execute("select `address_id` from address where `address_desc` = %s", (addressname))
        name = self.cursor.fetchone()
        if name:
            return name['address_id']
        else:
            return -1
