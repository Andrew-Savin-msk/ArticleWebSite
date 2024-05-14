"""
Модули моделей для Flask-приложения, включающие в себя определения моделей данных.

Определяет структуру таблиц базы данных для пользователей и статей, а также предоставляет
функциональность для загрузки данных пользователя. Использует flask_login для управления
сессиями пользователя и flask_sqlalchemy для взаимодействия с базой данных.

Classes:
    Article(db.Model): Представляет статью в блоге.
    Users(db.Model, UserMixin): Представляет пользователя в системе.

Functions:
    load_user(user_id): Возвращает объект пользователя по его идентификатору.
"""

from flask_login import UserMixin
from application import db, manager
from datetime import datetime


class Article(db.Model):

    """
    Модель статьи для хранения информации о публикациях в блоге.
    
    Attributes:
        __tablename__ (str): Название таблицы в базе данных.
        id (db.Column): Уникальный идентификатор статьи.
        user_id (db.Column): Идентификатор пользователя, создавшего статью.
        title (db.Column): Заголовок статьи.
        intro (db.Column): Вводный текст статьи.
        text (db.Column): Основной текст статьи.
        date (db.Column): Дата и время создания статьи.
    """

    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class Users(db.Model, UserMixin):

    """
    Модель пользователя для хранения информации о пользователях системы.
    
    Attributes:
        __tablename__ (str): Название таблицы в базе данных.
        id (db.Column): Уникальный идентификатор пользователя.
        login (db.Column): Логин пользователя, используемый для входа.
        encrypted_password (db.Column): Зашифрованный пароль пользователя.
        name (db.Column): Имя пользователя.
        articles (db.relationship): Связь с статьями, созданными пользователем.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)        
    articles = db.relationship('Article', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.login


@manager.user_loader
def load_user(user_id):

    """
    Загрузчик пользователя, используемый flask_login для получения экземпляра пользователя.
    
    Args:
        user_id: Уникальный идентификатор пользователя.
    
    Returns:
        Экземпляр класса Users, соответствующий пользователю с заданным идентификатором.
    """

    return Users.query.get(user_id)