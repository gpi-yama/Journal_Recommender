# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class JournalPipeline(object):

    def open_spider(self, spider):
        settings = spider.settings
        params = {
            #            'host': settings.get('MYSQL_HOST', 'local_host'),
            'db': settings.get('MYSQL_DATABASE', "journal"),
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
        date VARCHAR(200))''')

        self.conn.commit()

    def close_spider(self, spider):
        self.c.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        item = item
        items = dict(item)
        if item["abstract"] != []:
            self.c.execute('''
                    INSERT INTO items (title, author, date, abstract)
                    VALUES (%s, %s, %s, %s)
                    ''', (' '.join(items["title"]), ' '.join(items["author"]), ' '.join(items["date"]), ' '.join(items["abstract"])))

        return item
