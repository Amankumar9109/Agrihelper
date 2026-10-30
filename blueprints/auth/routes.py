from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        # Support both form post and json post
        data = request.form if request.form else (request.get_json() or {})
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html', error='Please provide both email and password.')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html', error='Invalid email or password.')

    return render_template('login.html')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.form if request.form else (request.get_json() or {})
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('auth.login'))

    if User.query.filter_by(email=email).first():
        flash('Email already registered. Please log in.', 'warning')
        return redirect(url_for('auth.login'))

    user = User(name=name, email=email, provider='local')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash('Account created successfully!', 'success')
    return redirect(url_for('main.home'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
