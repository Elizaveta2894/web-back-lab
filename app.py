from flask import Flask, url_for, request, redirect, render_template, abort, make_response, send_file, Response, abort
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
import datetime
import os
import random  # Добавлен импорт random

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)

@app.route('/start')
def start():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <link rel="stylesheet" href="''' + url_for('static', filename='main.css') + '''">
</head>
<body>
    <header>
        НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
    </header>

    <main>
        <h1>Лабораторные работы по WEB-программированию</h1>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3/">Третья лабораторная</a></li>
        </ol>
    </main>

    <footer>
        &copy; Стабровская Елизавета, ФБИ-33, 2025
    </footer>
</body>
</html>
'''

@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Главное меню</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
        }
        .menu-link {
            display: block;
            background: #0066cc;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 8px;
            margin: 15px 0;
            transition: all 0.3s ease;
            font-size: 18px;
        }
        .menu-link:hover {
            background: #0052a3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,102,204,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Главное меню</h1>
        <a href="/lab1" class="menu-link">Перейти к лабораторной работе 1</a>
        <a href="/lab2" class="menu-link lab2-link">Перейти к лабораторной работе 2</a>
    </div>
</body>
</html>
'''

@app.route('/error500')
def cause_500_error():
    """Обработчик, который вызывает различные типы ошибок сервера"""
    error_type = random.choice([1, 2, 3, 4, 5])
    
    if error_type == 1:
        result = 10 / 0
        return f"Деление на ноль: {result}"  # Это никогда не выполнится
    elif error_type == 2:
        result = "текст" + str(123)  # Исправлено: преобразование в строку
        return result
    elif error_type == 3:
        # Имитация ошибки NoneType
        obj = None
        if obj is None:
            abort(500)
        return "Этот код не выполнится"
    elif error_type == 4:
        lst = [1, 2, 3]
        if len(lst) <= 10:
            abort(500)
        result = lst[10]
        return f"Элемент списка: {result}"
    elif error_type == 5:
        # Попытка импорта несуществующего модуля
        abort(500)
    
    return "Неизвестный тип ошибки"

@app.errorhandler(500)
def internal_server_error(err):
    """Обработчик ошибки 500 с красивой страницей на русском языке"""
    error_page = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Внутренняя ошибка сервера - Ошибка 500</title>
        <style>
            /* ... ваш CSS стиль ... */
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">⚠️</div>
            <h1>500</h1>
            <h2>Внутренняя ошибка сервера</h2>
            
            <p>На сервере произошла непредвиденная ошибка. Наша команда уже уведомлена и работает над решением проблемы.</p>
            
            <div class="button-container">
                <button class="home-button" onclick="window.location.href='/'">🏠 На главную страницу</button>
                <button class="reload-button" onclick="window.location.reload()">🔄 Попробовать снова</button>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const container = document.querySelector('.error-container');
                container.style.opacity = '0';
                container.style.transform = 'translateY(30px)';
                
                setTimeout(() => {
                    container.style.transition = 'all 0.8s ease';
                    container.style.opacity = '1';
                    container.style.transform = 'translateY(0)';
                }, 100);
            });
        </script>
    </body>
    </html>
    """
    return error_page, 500

@app.errorhandler(404)
def not_found(error):
    # Создаем error_log, если его нет
    if 'error_log' not in globals():
        global error_log
        error_log = []
    
    log_entry = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': request.url,
        'error': str(error)
    }
    error_log.append(log_entry)
    
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, port=5000)