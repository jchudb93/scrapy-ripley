# -*- coding: utf-8 -*-
import scrapy

from ripley.items import RipleyItemLoader
from scrapy import Spider, Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

import ripley.utils as utils

class TvVideoSpider(scrapy.Spider):

    name = 'tv-video'

    allowed_domains = ['simple.ripley.com.pe']

    start_urls = [
        'https://simple.ripley.com.pe/tv-y-video/televisores/ver-todo-tv?source=menu',
        'https://simple.ripley.com.pe/tv-y-video/video-y-accesorios/ver-todo-video-y-accesorios?source=menu',
        'https://simple.ripley.com.pe/tv-y-video/audio-para-tv/ver-todo-audio-para-tv?source=menu',
        'https://simple.ripley.com.pe/tv-y-video/equipo-de-sonido/ver-todo-equipo-de-sonido?source=menu',
        'https://simple.ripley.com.pe/tv-y-video/audio-portatil/ver-todo-audio-portatil?source=menu',
        'https://simple.ripley.com.pe/tv-y-video/car-audio/ver-todo-car-audio?source=menu']

    tipos_productos = ['televisores', 'video-y-accesorios', 'audio-para-tv', 'sonido', 'audio-portatil', 'car-audio']

    def parse(self, response):

        for r in self.parse_items(response):
            yield r
        
        n_paginas = len(response.xpath('//div[has-class("catalog-page__footer-pagination")]//nav/ul[has-class("pagination")]//li').extract()) - 2
        
        for pagina in range(2, n_paginas + 1):

            url = f'{response.url}&page={pagina}'
            yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):

        tipo_producto = utils.obtener_tipo_producto(response.url, self.tipos_producto)
        categoria = 'tecnologia'
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