from flask import Blueprint, render_template, url_for, request, make_response, redirect, session, flash
import hashlib

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])  
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        
        if x2 == 0:
            return render_template('lab4/div.html', error='Деление на ноль невозможно!')
        
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/div.html', error='Введите корректные числа!')


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')  
    
    try:
        x1 = int(x1) if x1 != '' else 0
        x2 = int(x2) if x2 != '' else 0
        result = x1 + x2
        return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/sum.html', error='Введите корректные числа!')


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '1') 
    x2 = request.form.get('x2', '1') 
    
    try:
        x1 = int(x1) if x1 != '' else 1
        x2 = int(x2) if x2 != '' else 1
        result = x1 * x2
        return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/mul.html', error='Введите корректные числа!')


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/sub.html', error='Введите корректные числа!')


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
        
        if x1 == 0 and x2 == 0:
            return render_template('lab4/pow.html', error='Ноль в нулевой степени не определен!')
        
        result = x1 ** x2
        return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)
    
    except ValueError:
        return render_template('lab4/pow.html', error='Введите корректные числа!')


tree_count = 0
MAX_TREES = 10 

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', 
                             tree_count=tree_count, 
                             max_trees=MAX_TREES)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < MAX_TREES:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Alex', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Bob', 'gender': 'male'},
    {'login': 'tasia', 'password': '234', 'name': 'Tasia', 'gender': 'female'},
    {'login': 'anna', 'password': '343', 'name': 'Anna', 'gender': 'female'},
    {'login': 'liza', 'password': '456', 'name': 'Liza Stabrovskaya', 'gender': 'female'},
    {'login': 'maksim', 'password': '789', 'name': 'Maksim Gavrilov', 'gender': 'male'}
]

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def check_auth():
    return 'login' in session


def get_current_user():
    if 'login' in session:
        return next((user for user in users if user['login'] == session['login']), None)
    return None

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')

    if not login or not password or not name:
        return render_template('lab4/register.html', error='Все поля обязательны для заполнения')
    
    if password != password_confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают')
    
    if any(user['login'] == login for user in users):
        return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')
    
    new_user = {
        'login': login,
        'password': hash_password(password),
        'name': name,
        'gender': request.form.get('gender', 'male')
    }
    users.append(new_user)
    
    session['login'] = login
    return redirect('/lab4/users')

@lab4.route('/lab4/users')
def users_list():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    return render_template('lab4/users.html', users=users, current_user=current_user)

@lab4.route('/lab4/users/delete', methods=['POST'])
def delete_user():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_login = session['login']
    global users
    users = [user for user in users if user['login'] != current_login]
    
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users/edit', methods=['GET', 'POST'])
def edit_user():
    if not check_auth():
        return redirect('/lab4/login')
    
    current_user = get_current_user()
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)
    
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    if not login or not name:
        return render_template('lab4/edit_user.html', user=current_user, error='Логин и имя обязательны')

    if login != current_user['login'] and any(user['login'] == login for user in users):
        return render_template('lab4/edit_user.html', user=current_user, error='Пользователь с таким логином уже существует')

    for user in users:
        if user['login'] == current_user['login']:
            user['login'] = login
            user['name'] = name

            if password:
                if password != password_confirm:
                    return render_template('lab4/edit_user.html', user=user, error='Пароли не совпадают')
                user['password'] = hash_password(password)
            
            break

    session['login'] = login
    return redirect('/lab4/users')

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if check_auth():
            current_user = get_current_user()
            name = current_user['name'] if current_user else session['login']
            return render_template('lab4/login.html', name=name, authorized=True)
        else:
            return render_template('lab4/login.html', authorized=False)

    login_input = request.form.get('login')
    password = request.form.get('password')
    
    saved_login = login_input or ''
    
    if not login_input:
        return render_template('lab4/login.html', authorized=False, error='Не введён логин', login=saved_login)
    
    if not password:
        return render_template('lab4/login.html', authorized=False, error='Не введён пароль', login=saved_login)

    for user in users:
        if login_input == user['login'] and hash_password(password) == user['password']:
            session['login'] = login_input
            return redirect('/lab4/login')
            
    error = 'Неверный логин и/или пароль'
    return render_template('lab4/login.html', authorized=False, error=error, login=saved_login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите целое число')
    
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    
    if temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')

    if -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge.html', 
                         temperature=temp, 
                         snowflakes=snowflakes,
                         success=f'Установлена температура: {temp}°C')


@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain-order.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    prices = {
        'barley': 12000,   
        'oats': 8500,     
        'wheat': 9000,     
        'rye': 15000       
    }
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not grain_type:
        return render_template('lab4/grain-order.html', error='Выберите тип зерна')
    
    if not weight:
        return render_template('lab4/grain-order.html', error='Укажите вес заказа')
    
    try:
        weight_val = float(weight)
    except ValueError:
        return render_template('lab4/grain-order.html', error='Введите корректный вес')

    if weight_val <= 0:
        return render_template('lab4/grain-order.html', error='Вес должен быть больше 0')

    if weight_val > 100:
        return render_template('lab4/grain-order.html', error='Такого объёма сейчас нет в наличии')

    price_per_ton = prices[grain_type]
    total = weight_val * price_per_ton

    discount = 0
    if weight_val > 10:
        discount = total * 0.10
        total -= discount
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain-order.html', 
                         success=True,
                         grain_name=grain_name,
                         weight=weight_val,
                         total=total,
                         discount=discount,
                         has_discount=weight_val > 10)


