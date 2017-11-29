#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/mydatabase'


class Files(object):
    directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), '..', 'files')

    def __init__(self):
        self._files = self._read_all_files()

    def _read_all_files(self):
        dirt_name_json = {}
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            with open(file_path) as f:
                file_json = json.load(f)
                dirt_name_json[filename[:-5]] = file_json
        return dirt_name_json

    def get_title_list(self):
        return [item['title'] for item in self._files.values()]

    def get_name_list(self):
        return list(self._files.keys())

    def get_dirt_name_title(self):
        dirt_name_title = {}
        for name, file_json in self._files.items():
            dirt_name_title[name] = file_json['title']
        return dirt_name_title

    def get_json_by_filename(self, filename):
        return self._files.get(filename)


files = Files()


@app.route('/')
def index():
    # dirt_name = {}
    # name_list = files.get_name_list()
    # title_list = files.get_title_list()
    # for index in range(len(name_list)):
    #     dirt_name[name_list[index]] = title_list[index]
    return render_template('index.html', dirt_name_title=files.get_dirt_name_title())


@app.route('/files/<filename>')
def file(filename):
    file_json = files.get_json_by_filename(filename)
    if not file_json:
        abort(404)
    return render_template('file.html', file_json=file_json)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
