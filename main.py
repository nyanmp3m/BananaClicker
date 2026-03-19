import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


sys.path.insert(0, os.path.dirname(__file__))


from first_DB.users_data import db_session
from first_DB.users_data.about_users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'


db_path = os.path.join(os.path.dirname(__file__), 'instance', 'users.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)


db_session.global_init(db_path)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(session['user_id'])
    return render_template('profile.html', user=user)


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db_sess = db_session.create_session()


        existing_user = db_sess.query(User).filter(User.email == email).first()
        if existing_user:
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('login_page'))


        user = User()
        user.name = name
        user.email = email
        user.created_date = datetime.now()
        user.password = generate_password_hash(password)

        db_sess.add(user)
        db_sess.commit()

        session['user_id'] = user.id
        session['user_name'] = user.name

        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('login_page'))


@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'error')
            return redirect(url_for('login_page'))

    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login_page'))


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(session['user_id'])

    if request.method == 'POST':
        try:
            user.name = request.form['name']
            user.about = request.form['about']
            if request.form['birthday']:
                user.birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d')

            db_sess.commit()
            session['user_name'] = user.name
            flash('Профиль обновлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

    return render_template('edit_profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)