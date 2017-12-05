#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy

class ShiyanlouSpider(scrapy.Spider):
	name = 'shiyanlou-github'

	@property
	def start_urls(self):
		pass

	def parse(self, response):
		pass
