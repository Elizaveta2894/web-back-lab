from flask import Blueprint, render_template, url_for, request, make_response, redirect, session

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

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True

            user_data = next((user for user in users if user['login'] == session['login']), None)
            if user_data and 'name' in user_data:
                name = user_data['name']
            else:
                name = session['login']  
            return render_template('lab4/login.html', name=name, authorized=authorized)
        else:
            return render_template('lab4/login.html', authorized=False)

    login_input = request.form.get('login')
    password = request.form.get('password')

    saved_login = login_input or ''

    if not login_input:
        error = 'Не введён логин'
        return render_template('lab4/login.html', authorized=False, error=error, login=saved_login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', authorized=False, error=error, login=saved_login)


    for user in users:
        if login_input == user['login'] and password == user['password']:
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