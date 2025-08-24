from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Import models after initializing db to avoid circular imports
from models import User
@app.route('/')
def home():
    return "Welcome to the Daily Habit Tracker!"

if __name__ == '__main__':
    app.run(debug=True)