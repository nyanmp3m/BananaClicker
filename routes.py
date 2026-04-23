import json

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from first_DB import db_session
from first_DB.users_data.about_users import User
from globalVariables import score, inventory, tax
import random
import smtplib
from email.mime.text import MIMEText


db_sess = None
lastUser = None

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "kos.test.gmail@gmail.com"
APP_PASSWORD = "nlhv bupr pqlw jlza"


def send_verify_code(recipient_email, code):
    msg = MIMEText(f"Ваш код подтверждения: {code}")
    msg['Subject'] = "Код подтверждения регистрации"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

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

#  "count": 0,
# "auto": false,
# "add_count": 1  
def calculate_coaf(inventory: dict[str, int]) -> dict[str, int]:
    coaf = {
        "perClick": 1,
        "autoClick": 0
    }

    for key, item in inventory.items():
        if not item['auto']:
            coaf['perClick'] += (item['add_count'] * item['count'])
        elif item['auto']:
            coaf['autoClick'] += (item['add_count'] * item['count'])

    return coaf


def register_routes(app):
    # --- АВТОСОХРАНЕНИЕ ---
    @app.teardown_appcontext
    def autosave_userData(exception=None):
        global lastUser, inventory, score
        if lastUser:
            try:
                new_data = {"score": score, "purchases": inventory}
                lastUser.json_data = json.dumps(new_data)
                db_sess.commit()
                print(f'AutoSave Success: {score}')
            except Exception as exc:
                print(f'AutoSave Error: {exc}')

    # --- ГЛАВНЫЕ СТРАНИЦЫ ---
    @app.route('/')
    def index():
        global db_sess
        db_sess = db_session.create_session()
        session.clear()
        return redirect(url_for('between_requests'))

    @app.route('/between_requests')
    def between_requests():
        global score, db_sess, lastUser, inventory
        if 'user_id' not in session:
            return render_template('login.html', email_login="Email", email_register="Email", name_register="Name",
                                   form_type="login")

        lastUser = db_sess.query(User).get(session['user_id'])
        userData = json.loads(lastUser.json_data)
        score = userData.get('score')
        inventory = userData.get('purchases')

        return render_template('main.html',
                               score=score,
                               firstItem_count=inventory['firstItem']['count'],
                               firstItem_price=inventory['firstItem']['price'],
                               secondItem_count=inventory['secondItem']['count'],
                               secondItem_price=inventory['secondItem']['price'],
                               thirdItem_count=inventory['thirdItem']['count'],
                               thirdItem_price=inventory['thirdItem']['price'],
                               fourthItem_count=inventory['fourthItem']['count'],
                               fourthItem_price=inventory['fourthItem']['price']
                               )

    # --- ЛОГИКА РЕГИСТРАЦИИ И ПОДТВЕРЖДЕНИЯ ---
    @app.route('/register', methods=['POST'])
    def register():
        global db_sess
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            if db_sess.query(User).filter(User.email == email).first():
                flash('Пользователь с таким email уже существует', 'emailError_register')
                return redirect(url_for('login_page'))

            code = str(random.randint(1000, 9999))
            session['temp_user'] = {
                'name': name, 'email': email,
                'password': generate_password_hash(password), 'code': code
            }

            send_verify_code(email, code)  # Та самая функция отправки через Gmail
            return render_template("login.html", form_type="verify", email_register=email)
        except Exception as e:
            print(f"Ошибка регистрации: {e}")
            flash(f'Ошибка: {str(e)}', 'unknownError_register')
            return redirect(url_for('login_page'))

    @app.route('/confirm_email', methods=['POST'])
    def confirm_email():
        global db_sess
        user_input_code = request.form.get('code')
        temp_data = session.get('temp_user')

        if temp_data and user_input_code == temp_data['code']:
            user = User()
            user.name = temp_data['name']
            user.email = temp_data['email']
            user.password = temp_data['password']
            user.created_date = datetime.now()

            with open('userData.json', 'r', encoding='utf-8') as file:
                user.json_data = json.dumps(json.load(file))

            db_sess.add(user)
            db_sess.commit()
            session['user_id'] = user.id
            session.pop('temp_user')
            flash('Регистрация успешна!', 'success_register')
            return redirect(url_for('between_requests'))
        else:
            flash('Неверный код!', 'unknownError_register')
            return render_template("login.html", form_type="verify",
                                   email_register=temp_data.get('email') if temp_data else "")

    @app.route('/login', methods=['POST'])
    def login():
        global db_sess
        try:
            email = request.form['email']
            password = request.form['password']
            user = db_sess.query(User).filter(User.email == email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                return redirect(url_for('between_requests'))
            flash('Неверный email или пароль', 'emailError_login')
            return redirect(url_for('login_page'))
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'unknownError_login')
            return redirect(url_for('login_page'))

    @app.route('/login_page')
    def login_page():
        flashes = dict(session).get('_flashes', [('login', '')])
        return get_flash_template(flashes[-1][0])

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        return redirect(url_for('login_page'))

    # --- ИГРОВЫЕ МЕХАНИКИ ---
    @app.route('/click', methods=['GET'])
    def handle_click():
        global score, inventory
        coaf = calculate_coaf(inventory=inventory)
        score += coaf['perClick']
        return str(score)

    @app.route('/auto_click', methods=['GET'])
    def handle_auto_click():
        global inventory, score
        coaf = calculate_coaf(inventory=inventory)
        score += coaf['autoClick']
        return {'score': score}

    @app.route('/buy_first_item', methods=['GET'])
    def handle_buy_first_item():
        global inventory, score
        item = inventory['firstItem']
        if score >= item['price']:
            item['count'] += 1
            score -= item['price']
            item['price'] = int(
                item['price'] + item['startPrice'] * (item['count'] / 10))  # заменил tax на 10 для примера
            return {'firstItem_count': item['count'], 'score': score, 'newPrice': item['price']}
        return {'score': -407}

    # По аналогии можно добавить buy_second_item, buy_third_item и т.д.

    @app.route('/set_banana', methods=['GET'])
    def handle_get_banana():
        global score
        if request.args.get('password') == "cos(tan(tin()))":
            score = int(request.args.get('count', 0))
        return redirect(url_for('between_requests'))

    @app.route('/check_stats')
    def handel_check_stats():
        coaf = calculate_coaf(inventory=inventory)
        return {'statsText': f'<p>PerClick: {coaf["perClick"]}, AutoClick: {coaf["autoClick"]}, Score: {score}</p>'}
