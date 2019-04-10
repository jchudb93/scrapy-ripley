# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils

class RopaHombreSpider(scrapy.Spider):
    name = 'ropa-hombre'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = [
        'https://simple.ripley.com.pe/deporte/zapatillas-deportivas/hombre?source=menu',
        'https://simple.ripley.com.pe/calzado/calzado-hombre/todo-calzado-hombre?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/belleza-y-accesorios/relojes?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/belleza-y-accesorios/perfumes?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/polos?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/camisas?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/polerones?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/chompas?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/casacas?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/sacos?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/jeans?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/pantalones?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/shorts?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/ropa-de-bano?source=menu',
        'https://simple.ripley.com.pe/moda-hombre/ropa-hombre/ternos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/poleras-y-casacas?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/shorts?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/pantalones?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/camisetas-y-polos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/relojes-deportivos?source=menu',
        'https://simple.ripley.com.pe/deporte/ropa-deportiva-hombre/clubs-y-selecciones?source=menu',
        ]

    tipos_producto = [
            'calzado-hombre',
            'relojes',
            'perfumes',
            'polos',
            'camisas',
            'polerones',
            'chompas',
            'casacas',
            'sacos',
            'jeans',
            'pantalones',
            'shorts',
            'ropa-de-bano',
            'ternos',
            'poleras-y-casacas',
            'shorts',
            'pantalones',
            'camisetas-y-polos',
            'relojes-deportivos',
            'clubs-y-selecciones',
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
        categoria = 'ropa-hombre'
        print(tipo_producto)
        if ('zapatillas' in tipo_producto) or ('calzado-hombre' in tipo_producto):
            item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")]'
        else:
            item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item--moda catalog-product-item__container col-xs-12 col-sm-6 col-md-4 col-lg-4")]'
            
        # //*[@id="catalog-page"]/div/div[2]/div[3]/section/div/div/a[1]
        for producto in response.xpath(item_xpath):
            ripley_item_loader = RipleyItemLoader(response=response)
            nombre = producto.xpath('.//div[has-class("catalog-product-details__name")]/text()').extract()
            marca = ''
            precio = producto.xpath('.//div[has-class("catalog-prices")]/ul/li/text()').extract_first()
            url_imagen = producto.xpath('.//div[has-class("images-preview")]//img/@data-src').extract_first()
            ripley_item_loader.add_value('marca', marca)
            ripley_item_loader.add_value('nombre', nombre)
            ripley_item_loader.add_value('precio', precio)
            ripley_item_loader.add_value('imagen', url_imagen)
            ripley_item_loader.add_value('descripcion', '')
            ripley_item_loader.add_value('tipo_producto', tipo_producto)
            ripley_item_loader.add_value('categoria', categoria)
            ripley_item_loader.add_value('url', str(response.url))
        
            yield ripley_item_loader.load_item()

