#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import pandas as pd

def analysis(file, user_id):
	try:
	  	df = pd.read_json(file)
	except ValueError:
		return 0, 0
	
	item = df[df['user_id'] == user_id].minutes
	return item.count(), item.sum()

def analysis_raw(file, user_id):
	times = 0
	minutes = 0

	try:
		f = open(file)
		records = json.load(f)
		for item in records:
			if (item['user_id'] == user_id):
				times += 1
				minutes += item['minutes']
			else:
				continue
		f.close()
	except:
		pass
	return items, minutes