# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class SGermanTechJobsPipeline:
    def process_item(self, item, spider):
        return item


class SGermanTechJobsPipeline:
    def process_item(self, item, spider):
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        # Create or connect to the database file when the spider starts
        self.conn = sqlite3.connect('scraped_data.db')
        self.cursor = self.conn.cursor()
        # Create a table for your jobs
        # added UNIQUE to avoid dublicates
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                tags TEXT,
                company TEXT,
                apply_for_this_job TEXT,
                location TEXT,
                url TEXT UNIQUE
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        # Close the connection when the spider finishes
        self.conn.close()

    def process_item(self, item, spider):
        # This method is called for every item the spider scrapes
        # any dublicates are gonna be ingnored
        self.cursor.execute(
            'INSERT OR IGNORE INTO jobs (title, tags, company, apply_for_this_job, location, url) VALUES (?, ?, ?, ?, ?, ?)',
            (
                item.get('title'),
                str(item.get('tags', [])),
                item.get('company'),
                item.get('apply_for_this_job'),
                item.get('location'),
                item.get('url')
            )
        )
        self.conn.commit()
        return item