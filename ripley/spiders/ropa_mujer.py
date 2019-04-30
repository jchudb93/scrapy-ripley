# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils

class RopaMujerSpider(scrapy.Spider):
    name = 'ropa-mujer'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = [
        'https://simple.ripley.com.pe/calzado/zapatillas/urbana-mujer',
        'https://simple.ripley.com.pe/calzado/calzado-mujer/zapatos-de-vestir',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/relojes?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/carteras?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/perfumes?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/maquillaje?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/bijouterie-y-joyeria?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/belleza-y-accesorios/tratamiento?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-interior/todo-ropa-interior?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-interior/pijamas?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/chompas?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/casacas?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/polerones?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/blazers?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/blusas?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/polos?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/vestidos?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/faldas-y-shorts?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/jeans?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/pantalones?source=menu',
        'https://simple.ripley.com.pe/moda-mujer/ropa-mujer/ropa-de-bano?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/mallas-y-pantalones?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/polos-y-tops?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/poleras-y-casacas?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/shorts?source=menu',
        ]
    tipos_producto = [
        'zapatillas',
        'calzado-mujer',
        'relojes',
        'carteras',
        'perfumes',
        'maquillaje',
        'bijouterie-y-joyeria',
        'tratamiento',
        'ropa-interior',
        'pijamas'
        'chompas',
        'casacas',
        'polerones',
        'blazers',
        'blusas',
        'polos',
        'vestidos',
        'faldas-y-shorts',
        'jeans',
        'pantalones',
        'ropa-de-bano',
        'ropa-deportiva-mujer/mallas-y-pantalones',
        'ropa-deportiva-mujer/polos-y-tops',
        'ropa-deportiva-mujer/poleras-y-casacas',
        'ropa-deportiva-mujer/shorts'
        ]

    def parse(self, response):

        for r in self.parse_items(response):
            yield r
        
        n_paginas = len(response.xpath('//div[has-class("catalog-page__footer-pagination")]//nav/ul[has-class("pagination")]//li').extract()) - 2
        
        for pagina in range(2, n_paginas + 1):

            url = f'{response.url}&page={pagina}'
            yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):

        categoria = 'ropa-mujer'

        tipo_producto = utils.obtener_tipo_producto(response.url, self.tipos_producto)
        
        if ('zapatillas' in tipo_producto) or ('calzado-mujer' in tipo_producto):
            item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")]'
        else:
            item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item--moda catalog-product-item__container col-xs-12 col-sm-6 col-md-4 col-lg-4")]'
            
        item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item--moda catalog-product-item__container col-xs-12 col-sm-6 col-md-4 col-lg-4")]'
        # //*[@id="catalog-page"]/div/div[2]/div[3]/section/div/div/a[1]
        for producto in response.xpath(item_xpath):
            ripley_item_loader = RipleyItemLoader(response=response)
            nombre = producto.xpath('.//div[has-class("catalog-product-details__name")]/text()').extract()
            marca = ''
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

