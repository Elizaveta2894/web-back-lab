from flask import Flask, url_for, request, redirect, render_template, abort, make_response,  send_file, Response, abort
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
import datetime
import os
app = Flask(__name__)

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE']= os.getenv('DB_TYPE', 'postgres')


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
    elif error_type == 2:
        result = "текст" + 123
    elif error_type == 3:

        result = None.some_method()
    elif error_type == 4:

        lst = [1, 2, 3]
        result = lst[10]
    elif error_type == 5:

        import non_existent_module
    
    return "Эта строка никогда не будет достигнута"


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
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: #333;
                text-align: center;
            }
            
            .error-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                padding: 50px 40px;
                border-radius: 25px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
                max-width: 700px;
                margin: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .error-icon {
                font-size: 80px;
                margin-bottom: 20px;
                color: #ff6b6b;
            }
            
            h1 {
                font-size: 4em;
                margin: 10px 0;
                color: #ff6b6b;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                font-weight: 800;
            }
            
            h2 {
                font-size: 2em;
                margin: 10px 0 20px 0;
                color: #444;
                font-weight: 600;
            }
            
            p {
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 20px;
                color: #666;
            }
            
            .error-details {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 25px 0;
                border-left: 4px solid #ff6b6b;
                text-align: left;
            }
            
            .error-details h3 {
                color: #ff6b6b;
                margin-bottom: 10px;
            }
            
            .error-details ul {
                padding-left: 20px;
            }
            
            .error-details li {
                margin-bottom: 8px;
                color: #666;
            }
            
            .button-container {
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 30px;
            }
            
            .home-button {
                display: inline-block;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 15px 35px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 1.1em;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .reload-button {
                display: inline-block;
                background: linear-gradient(45deg, #00b894, #00a085);
                color: white;
                padding: 15px 35px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 1.1em;
                box-shadow: 0 5px 15px rgba(0, 184, 148, 0.4);
            }
            
            .home-button:hover, .reload-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            }
            
            .contact-info {
                margin-top: 30px;
                padding: 15px;
                background: #fff3cd;
                border-radius: 10px;
                border: 1px solid #ffeaa7;
            }
            
            .contact-info p {
                margin: 0;
                color: #856404;
                font-size: 1em;
            }
            
            @media (max-width: 768px) {
                .error-container {
                    padding: 30px 20px;
                    margin: 15px;
                }
                
                h1 {
                    font-size: 3em;
                }
                
                h2 {
                    font-size: 1.6em;
                }
                
                .button-container {
                    flex-direction: column;
                    align-items: center;
                }
                
                .home-button, .reload-button {
                    width: 100%;
                    max-width: 250px;
                }
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-icon">⚠️</div>
            <h1>500</h1>
            <h2>Внутренняя ошибка сервера</h2>
            
            <p>На сервере произошла непредвиденная ошибка. Наша команда уже уведомлена и работает над решением проблемы.</p>
            
            <div class="error-details">
                <h3>Что произошло?</h3>
                <ul>
                    <li>Сервер столкнулся с непредвиденной ситуацией</li>
                    <li>Произошла внутренняя ошибка при обработке вашего запроса</li>
                    <li>Это временная проблема, обычно она решается быстро</li>
                </ul>
            </div>
            
            <div class="error-details">
                <h3>Что вы можете сделать?</h3>
                <ul>
                    <li>Попробуйте обновить страницу через несколько минут</li>
                    <li>Вернитесь на главную страницу и попробуйте позже</li>
                    <li>Если проблема повторяется, свяжитесь с технической поддержкой</li>
                </ul>
            </div>
            
            <div class="button-container">
                <button class="home-button" onclick="window.location.href='/'">🏠 На главную страницу</button>
                <button class="reload-button" onclick="window.location.reload()">🔄 Попробовать снова</button>
            </div>
            
            <div class="contact-info">
                <p>Если проблема сохраняется, пожалуйста, свяжитесь с поддержкой: support@example.com</p>
            </div>
        </div>
        
        <script>
            // Плавное появление страницы
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


@app.errorhandler(404)
def not_found(error):
    global error_log
    if 'error_log' not in globals():
        error_log = []
    
    log_entry = {
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': request.url,
        'error': str(error)
    }
    error_log.append(log_entry)
    
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)