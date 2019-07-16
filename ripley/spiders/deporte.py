# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils

class DeporteSpider(scrapy.Spider):
    name = 'deporte'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = [
        'https://simple.ripley.com.pe/deporte/maquinas/elipticas?source=menu',
        'https://simple.ripley.com.pe/deporte/maquinas/trotadoras?source=menu',
        'https://simple.ripley.com.pe/deporte/maquinas/spinning?source=menu',
        'https://simple.ripley.com.pe/deporte/maquinas/bancas-y-abdominales?source=menu',
        'https://simple.ripley.com.pe/deporte/bicicletas/montaneras?source=menu',
        'https://simple.ripley.com.pe/deporte/bicicletas/bmx?source=menu',
        'https://simple.ripley.com.pe/deporte/bicicletas/infantiles?source=menu',
        'https://simple.ripley.com.pe/deporte/bicicletas/zapatillas?source=menu',
        'https://simple.ripley.com.pe/deporte/bicicletas/electricos?source=menu',
        'https://simple.ripley.com.pe/deporte/camping-y-tiempo-libre/skates-scooters-y-patines?source=menu',
        'https://simple.ripley.com.pe/deporte/camping-y-tiempo-libre/carpas?source=menu',
        'https://simple.ripley.com.pe/deporte/camping-y-tiempo-libre/mochilas-y-bolsos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/mallas-y-pantalones?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/polos-y-tops?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/poleras-y-casacas?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-mujer/shorts?source=menu',
        'https://simple.ripley.com.pe/deporte/zapatillas-deportivas/mujer?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/poleras-y-casacas?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/shorts?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/pantalones?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/camisetas-y-polos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/relojes-deportivos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/clubs-y-selecciones?source=menu',
        'https://simple.ripley.com.pe/deporte/zapatillas-deportivas/hombre?source=menu'
        ]

    tipos_producto = [
        'elipticas',
        'trotadoras',
        'spinning',
        'bancas-y-abdominales',
        'montaneras',
        'bmx',
        'infantiles',
        'zapatillas',
        'electricos',
        'skates-scooters-y-patines',
        'carpas',
        'mochilas-y-bolsos',
        'mujer/mallas-y-pantalones',
        'mujer/shorts',
        'zapatillas-deportivas/mujer',
        'hombre/poleras-y-casacas',
        'hombre/shorts',
        'hombre/pantalones',
        'hombre/camisetas-y-polos',
        'hombre/relojes-deportivos'
        'hombre/clubs-y-selecciones',
        'zapatillas-deportivas/hombre'
        ]
    
    def parse(self, response):

        for r in self.parse_items(response):
            yield r
        
        n_paginas = len(response.xpath('//div[has-class("catalog-page__footer-pagination")]//nav/ul[has-class("pagination")]//li').extract()) - 2
        
        for pagina in range(2, n_paginas + 1):

            # url = f'{response.url}&page={pagina}'
            url = '%s&page=%s' % (response.url, pagina)
            yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):

        
        tipo_producto = utils.obtener_tipo_producto(response.url, self.tipos_producto)
        categoria = 'deportes'
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

