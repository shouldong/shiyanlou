#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def datafigure(file):
	try:
	  	df = pd.read_json(file)
	except ValueError:
		return

	data = df.groupby('user_id').sum().head(100)
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_title('StudyData')
	ax.set_xlabel('User ID')
	ax.set_ylabel('Study Time')
	ax.plot(data.index, data.minutes)
	plt.show()


if __name__ == '__main__':
	datafigure("user_study.json")

