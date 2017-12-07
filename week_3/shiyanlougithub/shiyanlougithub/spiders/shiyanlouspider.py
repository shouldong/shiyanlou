#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class ShiyanlouSpider(scrapy.Spider):
	name = 'shiyanlougithub'

	@property
	def start_urls(self):
		url_tmpl = 'https://github.com/shiyanlou?tab=repositories&page={}'
		return (url_tmpl.format(i) for i in range(1, 5))

	def parse(self, response):
		for repository in response.css('li.public'):
			item = ShiyanlougithubItem()
			item['name'] = repository.css('div.mb-1 a::text').re_first("\n\s*(.*)")
			item['update_time'] = repository.xpath('.//relative-time/@datetime').extract_first()
			detail_url = response.urljoin(repository.xpath('.//a/@href').extract_first())
			request = scrapy.Request(detail_url, callback=self.parse_detail)
			request.meta['item'] = item
			yield request

	def parse_detail(self, response):
		item = response.meta['item']
		for detail in response.css('ul.numbers-summary li'):
			detail_text = detail.xpath('.//a/text()').re_first("\n\s*(.*)\n")
			detail_num = detail.xpath('.//span[@class="num text-emphasized"]/text()').re_first("\n\s*(.*)\n")
			if detail_text and detail_num:
				detail_num = detail_num.replace(',', '')
				if detail_text in ('commit', 'commits'):
					item['commits'] = int(detail_num)
				elif detail_text in ('branch', 'branches'):
					item['branches'] = int(detail_num)
				elif detail_text in ('release', 'releases'):
					item['releases'] = int(detail_num)
		yield item

		
