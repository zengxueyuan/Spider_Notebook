# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestprojectItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    age = scrapy.Field()
    score = scrapy.Field()
    pass


t = TestprojectItem()

t['name'] = '小象'
t['age'] = 39
t['score'] = 98

print(t)
print(t['name'])
print(t['age'])
print(t['score'])
