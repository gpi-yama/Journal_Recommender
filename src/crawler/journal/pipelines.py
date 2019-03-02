# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import datetime
import re


class JournalPipeline(object):

    def open_spider(self, spider):
        settings = spider.settings
        params = {
            #            'host': settings.get('MYSQL_HOST', 'local_host'),
            'db': settings.get('MYSQL_DATABASE', "journal2"),
            'user': settings.get('MYSQL_USER', "yamaguchir"),
            'passwd': settings.get('MYSQL_PASSWORD', ' '),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4')
        }

        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor()
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS items
        (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        author VARCHAR(200),
        abstract VARCHAR(5000),
        date VARCHAR(200),
        url VARCHAR(200),
        jname VARCHAR(200))''')

        self.conn.commit()

    def close_spider(self, spider):
        self.c.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        items = dict(item)
        title = 1
        num = 1
        try:
            a = items["title"][1]
            num = 1
        except:
            num = 0

        if items["title"] != []:
            strs = re.sub('\n', '', ' '.join(items["title"]))
            title = self.c.execute('''
                    SELECT title FROM items WHERE (title=%s)
                    ''', [strs])

        if title == 0:
            if items["abstract"] == []:
                items["abstract"] = ["None", ]

            if items["author"] == []:
                items["author"] = ["None", ]

            if items["url"] == []:
                items["url"] = ["None", ]

            if items["date"] == []:
                items["date"] = [datetime.datetime(1000, 1, 1, 0, 0)]

            if items["jname"] == []:
                items["jname"] = ["Journal of Fluid Mechanics", ]

            self.c.execute('''
                        INSERT INTO items
                        (title, author, date, abstract, url, jname)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (re.sub('\n', '', ' '.join(items["title"])),
                              re.sub('\n', '', ' , '.join(items["author"])),
                              re.sub('\n', '', items["date"][num]),
                              re.sub('\n', '', ' '.join(items["abstract"])),
                              re.sub('\n', '', ' '.join(items["url"])),
                              re.sub('\n', '', ' , '.join(items["jname"]))))

        return item
