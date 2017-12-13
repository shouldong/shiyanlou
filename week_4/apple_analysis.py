#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import pandas as pd

def quarter_volume(file):
	try:
		data = pd.read_csv(file)
	except ValueError:
		return

	s = data.Volume
	s.index = pd.to_datetime(data.Date)
	return s.resample('Q').sum().sort_values()[-2]


if __name__ == '__main__':
	quarter_volume('apple.csv')