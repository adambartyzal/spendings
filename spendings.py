from app import app, db
from app.models import User, Category, Transaction, Transaction_type

@app.shell_context_processor
def make_shell_context():
  return {
    'db': db,
    'User': User,
    'Category': Category,
    'Transaction': Transaction,
    'Transaction_type': Transaction_type
  }
