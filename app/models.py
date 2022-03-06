from app import db
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  note = db.Column(db.String(256))
  transactions = db.relationship('Transaction', backref='author', lazy='dynamic')

  def __repr__(self):
    return '<User {}>'.format(self.username)

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  description = db.Column(db.String(64))

  def __repr__(self):
    return '<Category {}>'.format(self.name)

class Transaction_type(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  description = db.Column(db.String(64))

  def __repr__(self):
    return '<Transaction type {}>'.format(self.name)

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  amount = db.Column(db.Float)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  type_id = db.Column(db.Integer, db.ForeignKey('category.id'))

  def __repr__(self):
    return '<Transaction {}>'.format(self.name)
