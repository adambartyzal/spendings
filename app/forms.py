from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields import DateField,DateTimeField
from wtforms.validators import ValidationError, DataRequired

class NewCategoryForm(FlaskForm):
  new_category_name = StringField('Name', validators=[DataRequired()])
  new_category_description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Add category')

class NewTransactionForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  amount = StringField('Amount', validators=[DataRequired()])
  type_id = SelectField('Type', validators=[DataRequired()])
  category_id = SelectField('Category', validators=[DataRequired()])
  date = DateField('Date', format='%Y-%m-%d', default=date.today)
  submit = SubmitField('Add transaction')

class DateRange(FlaskForm):
  date_from = DateField('From', format='%Y-%m-%d', default=date.today().replace(day=1))
  date_to = DateField('To', format='%Y-%m-%d', default=date.today)
  submit = SubmitField('Show selected')
