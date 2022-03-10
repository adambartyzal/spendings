from app import app, db
import time
import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.forms import NewTransactionForm, NewCategoryForm, DateRange
from app.models import Transaction, Transaction_type, Category
from wtforms import Label

@app.template_filter('date_only')
def datetime_format(value, format="%d. %m. %y"):
  return value.strftime(format)

@app.template_filter('month_text')
def datetime_format(value, format="%-d. %B"):
  return value.strftime(format)

@app.template_filter('debug')
def debug(text):
  print(f'Debug: {text}')
  return ''

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html', title='Home')

@app.route('/categories', methods=['GET'])
def categories():
  categories = Category.query.all()
  return render_template('categories.html', title='Categories', categories=categories)

@app.route('/category/<category_id>', methods=['GET'])
def category_detail(category_id):
  category = Category.query.get(category_id)
  return render_template('category.html', title='Category detail', category=category)

@app.route('/category/new', methods=['GET', 'POST'],)
def category_new():
  form = NewCategoryForm()
  if form.validate_on_submit():
    category = Category(name=form.new_category_name.data, description=form.new_category_description.data)
    db.session.add(category)
    db.session.commit()
    flash('Category {} added'.format(form.new_category_name.data))
    return redirect('/categories')
  return render_template('category_new.html', title='New Category', form=form)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
  form = DateRange()
  types = Transaction_type.query.all()
  categories = Category.query.all()
  transactions = db.session.query(Transaction).filter(Transaction.date.between( form.date_from.data, form.date_to.data + datetime.timedelta(days=1))).order_by("date").all()[::-1]
  if form.validate_on_submit():
    transactions = db.session.query(Transaction).filter(Transaction.date.between( form.date_from.data, form.date_to.data + datetime.timedelta(days=1))).all()
  return render_template('transactions.html', title='Transactions', transactions=transactions, types=types, categories=categories, form=form)

@app.route('/transaction/<transaction_id>', methods=['GET', 'POST', 'PUT'])
def transaction_detail(transaction_id):
  transaction = Transaction.query.get(transaction_id)
  form = NewTransactionForm(type_id = transaction.type_id, category_id=transaction.category_id)
  form.type_id.choices = [(type.id, type.name) for type in Transaction_type.query.all()]
  form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
  form.type_id.default = transaction.type_id
  form.category_id.default = transaction.category_id
  form.date.data = transaction.date
  form.name.data = transaction.name
  form.amount.data = transaction.amount
  form.submit.label = Label(form.submit.id, 'Edit transaction')
  if form.validate_on_submit():
    transaction.name = form.name.data
    transaction.amount = float(form.amount.data)
    transaction.type_id = int(form.type_id.data)
    transaction.category_id = int(form.category_id.data)
    transaction.date = form.date.data
    db.session.commit()
    flash(f'Transaction {form.name.data} changed')
    return redirect('/transactions')
  return render_template('transaction.html', title='Transaction detail', form=form)

@app.route('/transaction/new', methods=['GET', 'POST'],)
def transaction_new():
  form = NewTransactionForm()
  form.type_id.choices = [(type.id, type.name) for type in Transaction_type.query.all()]
  form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
  if form.validate_on_submit():
    transaction = Transaction(name=form.name.data, amount=float(form.amount.data), type_id=int(form.type_id.data), category_id=int(form.category_id.data), date=form.date.data)
    db.session.add(transaction)
    db.session.commit()
    flash(f'Transaction {form.name.data} added')
    return redirect('/transactions')
  return render_template('transaction.html', title='New Transaction', form=form)

@app.route('/transaction/<id>/delete', methods=['GET', 'DELETE'])
def transaction_delete(id):
  t = Transaction.query.get(id)
  if t:
    msg_text = 'Transaction successfully removed'
    db.session.delete(t)
    db.session.commit()
    flash(msg_text)
  return redirect(url_for('transactions'))

class Statement:
	def __init__(self):
		self.spent = 0
		self.gained = 0

def calculate_statement(transactions):
  s = Statement()
  for transaction in transactions:
    if (transaction.type_id == 1):
      s.spent += transaction.amount
    else:
      s.gained += transaction.amount
  return s

@app.route('/overview', methods=['GET', 'POST'])
def overview():
  form = DateRange()
  transactions = db.session.query(Transaction).filter(Transaction.date.between( form.date_from.data, form.date_to.data + datetime.timedelta(days=1))).all()
  statement = calculate_statement(transactions)
  if form.validate_on_submit():
    transactions = db.session.query(Transaction).filter(Transaction.date.between( form.date_from.data, form.date_to.data + datetime.timedelta(days=1))).all()
    statement = calculate_statement(transactions)
  return render_template('overview.html', title='Overview', transactions=transactions, form=form, statement=statement)
