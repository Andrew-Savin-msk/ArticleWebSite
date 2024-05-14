"""
Модуль конфигурации основного Flask приложения и его компонентов.

Этот модуль отвечает за инициализацию основных компонентов Flask приложения,
включая настройку базы данных через SQLAlchemy, управление сессиями пользователя
с помощью Flask-Login и настройку секретного ключа для сессий.

Attributes:
    app (Flask): Экземпляр приложения Flask, настроенный с секретным ключом и параметрами базы данных.
    db (SQLAlchemy): Экземпляр SQLAlchemy, связанный с приложением Flask для работы с базой данных.
    manager (LoginManager): Экземпляр LoginManager для управления сессиями пользователей в приложении Flask.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from application import models, routes

from application.models import Article, Users
with app.app_context():
    db.create_all()

    # user = Users(login = 'WeRReR', encrypted_password = 'yadsfgbaasgdf', name = 'Andrew')

    # db.session.add(user)
    # db.session.commit()

    # article1 = Article(user_id = Users.query.filter_by(login='WeRReR').first().id, title='art1', intro='Welcome To Art 1', text=' BibaBoba Art 1', date=datetime.utcnow())
    # db.session.add(article1)
    # article2 = Article(user_id = Users.query.filter_by(login='WeRReR').first().id, title='art2', intro='Welcome To Art 1', text=' BibaBoba Art 1', date=datetime.utcnow())
    # db.session.add(article2)
    # article3 = Article(user_id = Users.query.filter_by(login='WeRReR').first().id, title='art3', intro='Welcome To Art 1', text=' BibaBoba Art 1', date=datetime.utcnow())
    # db.session.add(article3)
    # article4 = Article(user_id = 345, title='art4', intro='Welcome To Art 1', text=' BibaBoba Art 1', date=datetime.utcnow())
    # db.session.add(article4)

    # db.session.commit()


    # print(Users.query.join(Article).add_columns(Users.name, Users.login, Article.title, Article.intro, Article.text, Article.date).filter(Users.id == Article.user_id).all())