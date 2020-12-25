from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    about_me = db.Column(db.Text())
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_moderator = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    ub = db.relationship('User_Book', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.login.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey(
        'writer.id'), nullable=False)
    title = db.Column(db.String(), index=True, nullable=False)
    genre = db.Column(db.String(), index=True, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    number_of_votes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='book', lazy='dynamic')
    ub = db.relationship('User_Book', backref='book', lazy='dynamic')


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True, nullable=False)
    additional_info = db.Column(db.Text(1024))
    books = db.relationship('Book', backref='author', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    text = db.Column(db.Text())
    datetime = db.Column(db.DateTime, default=datetime.utcnow)


class User_Book(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    mark = db.Column(db.Integer, default=0)
    # 1 - читал , 2 - читаю, 3 - хочу прочитать, 0 - вне списков
    category = db.Column(db.Integer, default=0)
