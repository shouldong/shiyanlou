#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    TEMPLATES_AUTO_RELOAD = True,
    SQLALCHEMY_TRACK_MODIFICATIONS = True,
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/shiyanlou'
)


db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).shiyanlou


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', uselist=False)
    content = db.Column(db.Text)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def add_tag(self, tag_name):
        article_item = mongo.article.find_one({'article_id': self.id})
        if article_item:
            tags = article_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
                mongo.article.update_one({'article_id': self.id}, {'$set': {'tags': tags}})
        else:
            tags = [tag_name]
            mongo.article.insert_one({'article_id': self.id, 'tags': tags})
        return tags

    def remove(self, tag_name):
        article_item = mongo.article.find_one({'article_id': self.id})
        if article_item:
            tags = article_item['tags']
            if tag_name in tags:
                tags.remove(tag_name)
                mongo.article.update_one({'article_id': self.id}, {'$set': {'tags': tags}})
            return tags
        return []

    @property
    def tags(self):
        article_item = mongo.article.find_one({'article_id': self.id})
        if article_item:
            return article_item['tags']
        return []


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    article = db.relationship('Article')

    def __init__(self, name):
        self.name = name


def insert_data():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    article1 = Article('Hello Java', datetime.utcnow(), java, 'Article Content - Java is cool!')
    article2 = Article('Hello Python', datetime.utcnow(), python, 'Article Content - Python is coooool!!!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(article1)
    db.session.add(article2)
    db.session.commit()
    article1.add_tag('tech')
    article1.add_tag('java')
    article1.add_tag('linux')
    article2.add_tag('tech')
    article2.add_tag('python')


def delete_data():
    db.drop_all()
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html', articles=Article.query.all())


@app.route('/articles/<article_id>')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    category = Category.query.get_or_404(article.category_id)
    return render_template('article.html', article=article, category=category)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
