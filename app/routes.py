from flask import render_template, flash, redirect
from app import app, db
from app.forms import LoginForm, NewCategoryForm, NewTransactionForm
from app.models import Category, Transaction, Transaction_type

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data))
    return redirect('/index')
  return render_template('login.html', title='Sign In', form=form)

@app.route('/categories', methods=['GET'])
def categories():
  categories = Category.query.all()
  return render_template('categories.html', title='Categories', categories=categories)

@app.route('/category/<category_id>', methods=['GET'])
def category_detail(category_id):
  category = Category.query.get(category_id)
  return render_template('category.html', title='Category detail', category=category)

@app.route('/category_new', methods=['GET', 'POST'],)
def category_new():
  form = NewCategoryForm()
  if form.validate_on_submit():
    category = Category(name=form.new_category_name.data, description=form.new_category_description.data)
    db.session.add(category)
    db.session.commit()
    flash('Category {} added'.format(form.new_category_name.data))
    return redirect('/categories')
  return render_template('category_new.html', title='New Category', form=form)

@app.route('/')
@app.route('/transactions', methods=['GET'])
def transactions():
  transactions = Transaction.query.all()
  types = Transaction_type.query.all()
  return render_template('transactions.html', title='Transactions', transactions=transactions, types=types)

@app.route('/transaction/<transaction_id>', methods=['GET'])
def transaction_detail(transaction_id):
  transaction = Transaction.query.get(transaction_id)
  types = Transaction_type.query.all()
  categories = Category.query.all()
  return render_template('transaction.html', title='Transaction detail', transaction=transaction, categories=categories, types=types)

@app.route('/transaction_new', methods=['GET', 'POST'],)
def transaction_new():
  form = NewTransactionForm()
  categories = Category.query.all()
  types = Transaction_type.query.all()
  if form.validate_on_submit():
    transaction = Transaction(name=form.name.data, amount=float(form.amount.data), type_id=int(form.type_id.data), category_id=int(form.category_id.data))
    db.session.add(transaction)
    db.session.commit()
    flash('Transaction {} added'.format(form.name.data))
    return redirect('/transactions')
  return render_template('transaction_new.html', title='New Transaction', form=form, categories=categories, types=types)
