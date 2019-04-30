# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from w3lib.html import remove_tags

_clean_spaces_re = re.compile(' +', re.U)


def clean_spaces(value):
    return _clean_spaces_re.sub(' ', value)

def clean_html(html):
    html = html.replace('\xa0', ' ')
    return html


class RipleyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    img = scrapy.Field()
    description = scrapy.Field()
    productType = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()

class RipleyItemLoader(ItemLoader):
    
    default_item_class = RipleyItem
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_spaces, clean_html, remove_tags, str.strip)
