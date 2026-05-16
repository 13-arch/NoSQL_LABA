import hashlib
import redis
import os
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first.db'
app.secret_key = b''

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=13)

db = SQLAlchemy(app)
Session(app)

cache_db = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Humans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(40))
    username = db.Column(db.String(20))
    email = db.Column(db.String(40))
    birthdate = db.Column(db.String(20))

with app.app_context():
    db.create_all()

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100).hex()


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Users.query.filter_by(username=username).first()
        
        if user and user.password == hash_password(password, username):
            session['username'] = username
            return redirect(url_for('home'))
        
        return render_template('login.html', error="Неверный логин или пароль")
    
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if Users.query.filter_by(username=username).first():
            return "Такой пользователь уже есть!"
            
        new_user = Users(username=username, password=hash_password(password, username))
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f"Ошибка при регистрации: {e}"
    
    return render_template('register.html')

@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        userdata = Humans(
            name=request.form.get('name'),
            surname=request.form.get('surname'),
            username=session['username'],
            email=request.form.get('email'),
            birthdate=request.form.get('birthdate')
        )
        db.session.add(userdata)
        db.session.commit()

        cache_db.delete(f"user_stats_{session['username']}")
        
        return "Данные успешно сохранены в БД!"
    
    return render_template('home.html', user=session['username'])


@app.route("/stats")
def stats():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    username = session['username']
    cache_key = f"user_stats_{username}"
    
    cached_data = cache_db.get(cache_key)
    
    if cached_data:
        source = "Взято ИЗ КЭША Redis (быстро)"
        result_text = cached_data
    else:
        source = "Загружено ИЗ БАЗЫ ДАННЫХ SQLite (медленно)"
        records_count = Humans.query.filter_by(username=username).count()
        result_text = f"Всего анкет создано пользователем: {records_count}"
        
        cache_db.setex(cache_key, 30, result_text)
        
    return f"<h3>Пользователь: {username}</h3><p>Источик данных: <b>{source}</b></p><p>Результат: {result_text}</p><p><a href='/home'>Назад домой</a></p>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(
        debug=True, 
        port=5000, 
        ssl_context=('cert.pem', 'key.pem')
    )