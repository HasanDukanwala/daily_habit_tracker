from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Daily Habit Tracker!"

if __name__ == '__main__':
    app.run(debug=True)