import json

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from first_DB import db_session
from first_DB.users_data.about_users import User
from globalVariables import score, inventory, tax

db_sess = None
lastUser = None

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
    @app.teardown_appcontext
    def autosave_userData(exception=None):
        global lastUser, inventory

        if lastUser:
            print(f'AutoSave: {score}')
            for keys, items in inventory.items():
                print(f'{keys}  : {items['count']}')

            try:
                print(inventory)

                new_data = {
                    "score": score,
                    "purchases": inventory
                }
                
                lastUser.json_data = json.dumps(new_data)

                db_sess.commit()
            except Exception as exc:
                print(f'Error: {exc}')


    @app.route('/')
    def index():
        global db_sess

        db_sess = db_session.create_session()
        session.clear()
        return redirect(url_for('between_requests'))
    
    @app.route('/set_banana', methods=['GET'])
    def handle_get_banana():
        global score
        try:
            newBanana_count = int(request.args.get('count'))
            score = newBanana_count

            print(f'Было установленно новое кол-во бананов {score}')

            return redirect(url_for('between_requests'))

        except Exception as exc:
            print(f'Error: {exc}')

    
    @app.route('/click', methods=['GET'])
    def handle_click():
        global score, inventory

        coaf = calculate_coaf(inventory=inventory)

        score += coaf['perClick']
        return str(score)
    
    @app.route('/buy_first_item', methods=['GET'])
    def handle_buy_first_item():
        global inventory, score

        if score - inventory['firstItem']['price'] >= 0:
            inventory['firstItem']['count'] += 1
            score -= inventory['firstItem']['price']

            inventory['firstItem']['price'] = int(inventory['firstItem']['price'] + inventory['firstItem']['startPrice'] * (inventory['firstItem']['count'] / tax))

            return {'firstItem_count': inventory['firstItem']['count'], 'score': score, 'newPrice':  inventory['firstItem']['price']}
        
        elif score - inventory['firstItem']['price'] < 0:
            return {'firstItem_count': inventory['firstItem']['count'], 'score': -407, 'newPrice': inventory['firstItem']['price']}
        
    @app.route('/buy_second_item', methods=['GET'])
    def handle_buy_second_item():
        global inventory, score
        
        if score - inventory['secondItem']['price'] >= 0:
            inventory['secondItem']['count'] += 1
            score -= inventory['secondItem']['price']

            inventory['secondItem']['price'] = int(inventory['secondItem']['price'] + inventory['secondItem']['startPrice'] * (inventory['secondItem']['count'] / tax))

            return {'secondItem_count': inventory['secondItem']['count'], 'score': score, 'newPrice': inventory['secondItem']['price']}
        
        elif score - inventory['secondItem']['price'] < 0:
            return {'secondItem_count': inventory['secondItem']['count'], 'score': -407, 'newPrice': inventory['secondItem']['price']}
    
    @app.route('/buy_third_item', methods=['GET'])
    def handle_buy_third_item():
        global inventory, score
        
        if score - inventory['thirdItem']['price'] >= 0:
            inventory['thirdItem']['count'] += 1
            score -= inventory['thirdItem']['price']

            inventory['thirdItem']['price'] = int(inventory['thirdItem']['price'] + inventory['thirdItem']['startPrice'] * (inventory['thirdItem']['count'] / tax))

            return {'thirdItem_count': inventory['thirdItem']['count'], 'score': score, 'newPrice': inventory['thirdItem']['price']}
        
        elif score - inventory['thirdItem']['price'] < 0:
            return {'thirdItem_count': inventory['thirdItem']['count'], 'score': -407, 'newPrice': inventory['thirdItem']['price']}
        
    @app.route('/auto_click', methods=['GET'])
    def handle_auto_click():
        global inventory, score

        coaf = calculate_coaf(inventory=inventory)
        score += coaf['autoClick']
        
        print(f'Auto CLICK: {coaf['autoClick']}')

        return {'score': score}
    
    @app.route('/super_banana_click', methods=['GET'])
    def handle_super_banana_click():
        global inventory, score

        coaf = calculate_coaf(inventory=inventory)
        super_banana = coaf['autoClick'] * 100 + coaf['perClick'] * 100
        score += super_banana

        return {'score': score}

    @app.route('/between_requests')
    def between_requests():
        global score, db_sess, lastUser, inventory

        if 'user_id' not in session:
            return render_template('login.html', 
                                   email_login="Email", 
                                   email_register="Email", 
                                   name_register="Name",
                                   form_type = "login")
        
        lastUser = db_sess.query(User).get(session['user_id'])
        userData = json.loads(lastUser.json_data)
        userScore = userData.get('score')

        print(userData)
        print("Last USer gENERATED")

        score = userScore
        inventory = userData.get('purchases')

        return render_template('main.html', score=userScore, firstItem_count=inventory['firstItem']['count'], firstItem_price=inventory['firstItem']['price'],
                                                             secondItem_count=inventory['secondItem']['count'], secondItem_price=inventory['secondItem']['price'],
                                                             thirdItem_count=inventory['thirdItem']['count'], thirdItem_price=inventory['thirdItem']['price'])

    @app.route('/login_page')
    def login_page():
        session_data = dict(session)
        flashes = session_data.get('_flashes')
        flash_lastKey = flashes[-1][0]

        return get_flash_template(flash_lastKey)

    @app.route('/register', methods=['POST'])
    def register():
        global db_sess

        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            existing_user = db_sess.query(User).filter(User.email == email).first()
            if existing_user:
                flash('Пользователь с таким email уже существует', 'emailError_register')
                return redirect(url_for('login_page'))

            user = User()
            user.name = name
            user.email = email
            user.created_date = datetime.now()
            user.password = generate_password_hash(password)
            
            with open('userData.json', 'r', encoding='utf-8') as file:
                json_content = json.load(file)
            json_str = json.dumps(json_content)

            user.json_data = json_str

            db_sess.add(user)
            db_sess.commit()

            session['user_id'] = user.id
            session['user_name'] = user.name

            flash('Регистрация прошла успешно!', 'success_register')
            return redirect(url_for('between_requests'))

        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'unknownError_register')
            print(e)
            return redirect(url_for('login_page'))

    @app.route('/login', methods=['POST'])
    def login():
        global db_sess

        try:
            email = request.form['email']
            password = request.form['password']
            user = db_sess.query(User).filter(User.email == email).first()

            password_comfirm = user and check_password_hash(user.password, password)

            if password_comfirm:
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