# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils


class HogarSpider(scrapy.Spider):
    name = 'hogar'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = [
        'https://simple.ripley.com.pe/hogar/muebles/sofas-y-juegos-de-sala?source=menu',
        'https://simple.ripley.com.pe/hogar/muebles/mesas-varias?source=menu',
        'https://simple.ripley.com.pe/muebles/comedor-y-bar/ver-todo-comedor-y-bar',
        'https://simple.ripley.com.pe/hogar/organizacion/escritorios?source=menu',
        'https://simple.ripley.com.pe/muebles/muebles-de-dormitorio/roperos',
        'https://simple.ripley.com.pe/hogar/cocina-y-barbecue/juegos-de-ollas?source=menu',
        'https://simple.ripley.com.pe/hogar/cocina-y-barbecue/ollas-y-sartenes?source=menu',
        'https://simple.ripley.com.pe/hogar/cocina-y-barbecue/horno-y-reposteria?source=menu',
        'https://simple.ripley.com.pe/hogar/menaje-de-mesa/vajillas?source=menu',
        'https://simple.ripley.com.pe/hogar/menaje-de-mesa/cubiertos?source=menu',
        'https://simple.ripley.com.pe/hogar/alfombras/ver-todo-alfombras?source=menu',
        'https://simple.ripley.com.pe/hogar/lamparas/ver-todo-lamparas?source=menu',
        'https://simple.ripley.com.pe/hogar/arte-de-pared/cuadros?source=menu',
        'https://simple.ripley.com.pe/hogar/arte-de-pared/espejos?source=menu',
        'https://simple.ripley.com.pe/hogar/regalos/juegos-de-mesa?source=menu',
        'https://simple.ripley.com.pe/hogar/regalos/decoracion?source=menu',
        'https://simple.ripley.com.pe/hogar/regalos/marcos-de-fotos?source=menu',
        'https://simple.ripley.com.pe/dormitorio/ropa-de-cama/edredones-y-sham',
        'https://simple.ripley.com.pe/dormitorio/ropa-de-cama/cubrecamas-y-sham'
    ]

    tipos_producto = [
        'sofas',
        'mesas',
        'comedor',
        'escritorios',
        'roperos',
        'juegos-de-ollas',
        'ollas-y-sartenes',
        'horno-y-reposteria',
        'vajillas',
        'cubiertos',
        'alfombras',
        'lamparas',
        'cuadros',
        'espejos',
        'juegos-de-mesa',
        'decoracion',
        'marcos-de-fotos',
        'edredones',
        'cubrecamas'
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
        categoria = 'hogar'
        item_xpath = '//div//a[has-class("catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")]'
        # //*[@id="catalog-page"]/div/div[2]/div[3]/section/div/div/a[1]
        for producto in response.xpath(item_xpath):
            ripley_item_loader = RipleyItemLoader(response=response)
            marca = producto.xpath('.//div[has-class("brand-logo")]/span/text()').extract()
            nombre = producto.xpath('.//div[has-class("catalog-product-details__name")]/text()').extract()
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
