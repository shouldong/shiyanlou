#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask


def create_app():
    app = Flask('rmon')
    file = os.environ.get('RMON_CONFIG')
    content = ''
    try:
        with open(file) as f:
            for l in f:
                l = l.strip()
                if l.startswith('#'):
                    continue
                else:
                    content += l
    except:
        return app

    try:
        configJson = json.loads(content)
    except:
        return app

    for key in configJson:
        app.config[key.upper()] = configJson.get(key)
    return app
