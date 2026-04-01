from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from first_DB import db_session
from first_DB.users_data.about_users import User

def get_flash_template(key):
    if key == "emailError_register":
        return render_template("login.html",
                               email_login="Email",
                               email_register="Такой email занят",
                               name_register="Name",
                               form_type = "register")
    elif key == "unknownError_register":
        return render_template("login.html",
                               email_login="Email",
                               email_register="Ошибка регистрации",
                               name_register="Ошибка регистрации",
                               form_type = "register")
    elif key == "emailError_login":
        return render_template("login.html",
                               email_login="Неверный email или password",
                               email_register="Email",
                               name_register="Name",
                               form_type = "login")
    elif key == "unknownError_login":
        return render_template("login.html",
                               email_login="Ошибка входа",
                               email_register="Email",
                               name_register="Name",
                               form_type = "login")
    elif key == "success_register":
        return render_template("login.html",
                               email_login="Email",
                               email_register="Email",
                               name_register="Name",
                               form_type = "login"),
    elif key == "success_logout":
        return render_template("login.html",
                               email_login="Email",
                               email_register="Email",
                               name_register="Name",
                               form_type = "login")
    elif key == "success_login":
        return render_template("main.html")
    else:
        return "Последний флэш без нормального ключа..."

def register_routes(app):
    @app.route('/')
    def index():
        session.clear()
        return redirect(url_for('between_requests'))

    @app.route('/between_requests')
    def between_requests():
        if 'user_id' not in session:
            return render_template('login.html', 
                                   email_login="Email", 
                                   email_register="Email", 
                                   name_register="Name",
                                   form_type = "login")
        
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(session['user_id'])
        return render_template('main.html')

    @app.route('/login_page')
    def login_page():
        session_data = dict(session)
        flashes = session_data.get('_flashes')
        flash_lastKey = flashes[-1][0]

        return get_flash_template(flash_lastKey)

    @app.route('/register', methods=['POST'])
    def register():
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            db_sess = db_session.create_session()
            existing_user = db_sess.query(User).filter(User.email == email).first()
            if existing_user:
                flash('Пользователь с таким email уже существует', 'emailError_register')
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

            flash('Регистрация прошла успешно!', 'success_register')
            return redirect(url_for('between_requests'))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'unknownError_register')
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
                flash('Вы успешно вошли!', 'success_login')
                return redirect(url_for('between_requests'))
            else:
                flash('Неверный email или пароль', 'emailError_login')
                return redirect(url_for('login_page'))
            
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'unknownError_login')
            return redirect(url_for('login_page'))

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        flash('Вы вышли из системы', 'success_logout')
        return redirect(url_for('login_page'))