from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class NewCategoryForm(FlaskForm):
  new_category_name = StringField('Name', validators=[DataRequired()])
  new_category_description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Add category')

class NewTransactionForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  amount = StringField('Amount', validators=[DataRequired()])
  type_id = StringField('Type id', validators=[DataRequired()])
  category_id = StringField('Category id', validators=[DataRequired()])
  submit = SubmitField('Add transaction')
