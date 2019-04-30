# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils


class InfantilSpider(scrapy.Spider):
    name = 'infantil'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = [
        'https://simple.ripley.com.pe/infantil/jugueteria/juguetes-para-ninas?source=menu',
        'https://simple.ripley.com.pe/infantil/jugueteria/juguetes-para-ninos?source=menu',
        'https://simple.ripley.com.pe/infantil/jugueteria/pre-escolar-y-bebes?source=menu',
        'https://simple.ripley.com.pe/infantil/juegos-de-exterior/bicicletas-ninos?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/coches?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/sillas-de-auto?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/cunas-y-corrales?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/sillas-de-comer?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/bano?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/alimentacion-y-lactancia?source=menu',
        'https://simple.ripley.com.pe/infantil/maternidad/lactancia?source=menu',
        'https://simple.ripley.com.pe/infantil/maternidad/extractores?source=menu',
        'https://simple.ripley.com.pe/infantil/maternidad/brasiers-para-lactancia?source=menu',
        'https://simple.ripley.com.pe/infantil/maternidad/esterilizadores-y-calentadores?source=menu',
        'https://simple.ripley.com.pe/infantil/mundo-bebe/biberones-y-chupones',
    ]

    tipos_producto = [
        'juguetes-para-ninas',
        'juguetes-para-ninos',
        'pre-escolar-y-bebes',
        'bicicletas-para-ninos',
        'coches',
        'sillas-de-auto',
        'cunas-y-corrales',
        'sillas-de-comer',
        'bano',
        'alimentacion-y-lactancia'
        'lactancia',
        'extractores',
        'brasiers-para-lactancia',
        'esterilzadores-y-calentadores',
        'biberones-y-chupones',
        'bolsos-y-cambiadores'
        ]

    def parse(self, response):

        for r in self.parse_items(response):
            yield r
        
        n_paginas = len(response.xpath('//div[has-class("catalog-page__footer-pagination")]//nav/ul[has-class("pagination")]//li').extract()) - 2
        
        for pagina in range(2, n_paginas + 1):

            url = f'{response.url}&page={pagina}'
            yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):
        
        tipo_producto = utils.obtener_tipo_producto(response.url, self.tipos_producto)
        categoria = 'infantil'
        item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")]'
        # //*[@id="catalog-page"]/div/div[2]/div[3]/section/div/div/a[1]
        for producto in response.xpath(item_xpath):
            ripley_item_loader = RipleyItemLoader(response=response)
            marca = producto.xpath('.//div[has-class("brand-logo")]/span/text()').extract()
            nombre = producto.xpath('.//div[has-class("catalog-product-details__name")]/text()').extract()
            precio = producto.xpath('.//div[has-class("catalog-prices")]/ul/li/text()').extract_first()
            url_imagen = producto.xpath('.//div[has-class("images-preview")]//img/@data-src').extract_first()
            ripley_item_loader.add_value('brand', marca)
            ripley_item_loader.add_value('name', nombre)
            ripley_item_loader.add_value('price', precio)
            ripley_item_loader.add_value('img', url_imagen)
            ripley_item_loader.add_value('description', '')
            ripley_item_loader.add_value('productType', tipo_producto)
            ripley_item_loader.add_value('category', categoria)
            ripley_item_loader.add_value('url', str(response.url))
        
            yield ripley_item_loader.load_item()

