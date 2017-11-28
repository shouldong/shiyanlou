#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from collections import namedtuple
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

FileDirt = namedtuple('FileDirt', ['dirt_name_title', 'dirt_name_json'])

class Files(object):

	directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), '..', 'files')

	def __init__(self):
		self._files = self._read_all_files()

	def _read_all_files(self):
		dirt_name_title = {}
		dirt_name_json = {}
		for filename in os.listdir(self.directory)
			file_path = os.path.join(self.directory, filename)
			with open(file_path) as f:
				file_json = json.load(f)
				dirt_name_json[filename[:-5]] = file_json
				dirt_name_title[filename[:-5]] = file_json.title
		return FileDirt(dirt_name_title, dirt_name_json)

	def get_title_list(self):
		return self._files.dirt_name_title

	def get_json_by_filename(self, filename):
		return self._files.dirt_name_json.get(filename)

files = Files()

@app.route('/')
def index():
	return render_template('index.html', title_list = files.get_title_list)

@app.route('/files/<filename>')
def file(filename):
	file_json = files.get_json_by_filename(filename)
	if not file_json:
		abort(404)
	return render_template('file.html', file_json = file_json)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
		

if __name__ == '__main__':
	app.run()