#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'

db = SQLAlchemy(app)


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
    app.run(debug=True)
