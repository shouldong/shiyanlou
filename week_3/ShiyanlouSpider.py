#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy

class ShiyanlouSpider(scrapy.Spider):
	name = 'shiyanlou-github'

	@property
	def start_urls(self):
		url_tmpl = "https://github.com/shiyanlou?tab=repositories&page={}"
		return (url_tmpl.format(i) for i in range(1, 5))

	def parse(self, response):
		for repository in response.css('li.public'):
			yield {
				'name': repository.css('div.mb-1 a::text').extract_first(),
				'update_time': repository.xpath('.//relative-time/@datetime').extract_first()
			}
		
