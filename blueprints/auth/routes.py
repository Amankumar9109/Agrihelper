import os
import secrets
import urllib.parse
import requests
from flask import render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    next_page = request.args.get('next')
    if next_page:
        session['next_url'] = next_page

    if request.method == 'POST':
        data = request.form if request.form else (request.get_json() or {})
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html', error='Please provide both email and password.')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.name}!', 'success')
            redirect_to = session.pop('next_url', None) or url_for('main.home')
            return redirect(redirect_to)
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

    if len(password) < 6:
        flash('Password must be at least 6 characters long.', 'danger')
        return redirect(url_for('auth.login'))

    if User.query.filter_by(email=email).first():
        flash('An account with this email already exists. Please log in.', 'warning')
        return redirect(url_for('auth.login'))

    user = User(
        name=name,
        email=email,
        provider='local',
        avatar_url=f"https://ui-avatars.com/api/?name={urllib.parse.quote(name)}&background=15803d&color=fff"
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)
    flash(f'Welcome to AgriHelper, {user.name}! Your account is ready.', 'success')
    redirect_to = session.pop('next_url', None) or url_for('main.home')
    return redirect(redirect_to)

@auth_bp.route('/google')
def google_login():
    """Initiate Google OAuth 2.0 flow"""
    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')

    # If Google credentials are not yet configured in .env
    if not client_id or not client_secret:
        # If in debug/dev, offer simulated login so testing is never blocked
        if current_app.config.get('DEBUG', True):
            flash('Google Client ID/Secret not set in .env. Logging in via Dev Google Account for testing.', 'info')
            return redirect(url_for('auth.google_dev_login'))
        else:
            flash('Google Authentication is currently being configured. Please use email/password.', 'warning')
            return redirect(url_for('auth.login'))

    # Generate state to protect against CSRF
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    redirect_uri = url_for('auth.google_callback', _external=True)

    google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'prompt': 'select_account',
        'access_type': 'offline'
    }

    auth_url = f"{google_auth_endpoint}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@auth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth 2.0 callback and token exchange"""
    # Verify state token against CSRF
    returned_state = request.args.get('state')
    saved_state = session.pop('oauth_state', None)

    if not returned_state or returned_state != saved_state:
        flash('Authentication state mismatch. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

    code = request.args.get('code')
    if not code:
        err = request.args.get('error', 'Unknown OAuth error')
        flash(f'Google sign-in was cancelled or failed: {err}', 'danger')
        return redirect(url_for('auth.login'))

    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = url_for('auth.google_callback', _external=True)

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    try:
        token_response = requests.post(token_url, data=token_data, timeout=10)
        token_json = token_response.json()

        if 'error' in token_json:
            flash(f"OAuth Token Error: {token_json.get('error_description', token_json['error'])}", 'danger')
            return redirect(url_for('auth.login'))

        access_token = token_json.get('access_token')

        # Fetch user info from Google
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        userinfo_response = requests.get(
            userinfo_url,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=10
        )
        user_info = userinfo_response.json()

        google_id = user_info.get('sub')
        email = user_info.get('email', '').lower()
        name = user_info.get('name', 'AgriHelper User')
        picture = user_info.get('picture')

        # Find or create User
        user = User.query.filter((User.google_id == google_id) | (User.email == email)).first()

        if user:
            user.google_id = google_id
            user.provider = 'google'
            if picture:
                user.avatar_url = picture
            db.session.commit()
        else:
            user = User(
                google_id=google_id,
                email=email,
                name=name,
                avatar_url=picture,
                provider='google'
            )
            db.session.add(user)
            db.session.commit()

        login_user(user, remember=True)
        flash(f'Signed in with Google as {user.name}!', 'success')
        redirect_to = session.pop('next_url', None) or url_for('main.home')
        return redirect(redirect_to)

    except Exception as e:
        flash(f'Authentication failed: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/google/dev-demo')
def google_dev_login():
    """Development helper: simulated Google login for rapid testing without external OAuth credentials"""
    email = "google.farmer.demo@agrihelper.in"
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            email=email,
            name="Aman Kumar (Google)",
            avatar_url="https://lh3.googleusercontent.com/a/default-user=s96-c",
            google_id="demo-google-oauth-id-12345",
            provider="google"
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    flash(f"Logged in with Google Demo Account as {user.name}!", "success")
    redirect_to = session.pop('next_url', None) or url_for('main.home')
    return redirect(redirect_to)

@auth_bp.route('/logout')
@login_required
def logout():
    name = current_user.name
    logout_user()
    flash(f'You have been logged out. See you soon, {name}!', 'info')
    return redirect(url_for('main.home'))
