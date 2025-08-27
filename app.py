from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask import render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_daily_habit_secret_key'  # Change this in production to strong secret key

#  Initialize the database with the app
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# The user loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# ---- Database Models ----
# Import models after initializing db to avoid circular imports
from models import User

# A page to run when user visits the root URL (Home page)
@app.route('/')
def home():
    if current_user.is_authenticated:
        return f"Hello, {current_user.email}! Welcome to your Daily Habit Tracker."
    return "<h1>Hello, Guest.</h1><a href='register'>Register</a> or <a href='login'>Login</a>"

# --- User Registration Route ---
# A page to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already exists. Please choose a different email or login.', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create a new user and add to the database
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success') 
        return redirect(url_for('login'))
    
    return render_template('register.html')

# -- User Login Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# -- User Logout Route ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)