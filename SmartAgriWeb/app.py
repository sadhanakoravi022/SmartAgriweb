"""
SmartAgriWeb - Flask Application
Agricultural management dashboard with water, crop, analytics, and inventory tracking.
"""

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smartagriweb-secret-key-change-in-production'


# Simple auth check (replace with real DB/Flask-Login later)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============ Auth Routes ============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = request.form.get('username', '')
        passwd = request.form.get('password', '')
        if user == 'admin' and passwd == 'admin123':
            session['logged_in'] = True
            session['username'] = user
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        if password != confirm:
            flash('Passwords do not match!', 'error')
        else:
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ============ Dashboard Routes ============

@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('dashboard/home.html')


@app.route('/crop')
@login_required
def crop():
    return render_template('dashboard/crop.html')


@app.route('/water')
@login_required
def water():
    return render_template('dashboard/water.html')


@app.route('/analytics')
@login_required
def analytics():
    return render_template('dashboard/analytics.html')


@app.route('/inventory')
@login_required
def inventory():
    return render_template('dashboard/inventory.html')


# Legacy redirect for index.html
@app.route('/index.html')
def index_redirect():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
