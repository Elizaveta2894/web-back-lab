from flask import Flask, url_for, request, redirect, render_template, abort, make_response,  send_file, Response
import datetime
import os
app = Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<! doctype html>" 
        "<html>"
        "   <body>"  
        "       <h1>web-сервер на flask</hl>" 
                <p><a href ="/author">author</a></p>
        "   </body>" 
        "</html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8"
            }


@app.route("/lab1/author")
def author():
    name = 'Стабровская Елизавета Евгеньевна'
    group= 'ФБИ-33'
    faculty = 'ФБ'

    return """<! doctype html>
        <html>
            <body>
                <p>Студент: """+name+"""</p>
                <p>Группа: """+group+"""</p>
                <p>Факультет: """+faculty+"""</p>
                <a href ="/web">web</a>
            </body>
        </html>"""



@app.route('/lab1/image')
def image():
    css_url = url_for('static', filename='lab1.css')
    
    html_content = f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_url}">
        <title>Леопард</title>
    </head>
    <body>
        <div class="container">
            <h1>Леопард</h1>
            <img src="/static/i.webp" alt="Леопард">
            <p>Леопард(барс, пантера, лат. Panthera pardus) — вид хищных млекопитающих семейства кошачьих.</p>
        </div>
    </body> 
</html>
'''
    
    # Создаем response с HTML контентом
    response = make_response(html_content)
    
    # Добавляем стандартный заголовок Content-Language
    response.headers['Content-Language'] = 'ru'  # Язык контента - русский
    
    # Добавляем кастомные нестандартные заголовки
    response.headers['X-Animal-Type'] = 'Big Cat'  # Тип животного
    response.headers['X-Page-Theme'] = 'Wildlife'  # Тема страницы
    response.headers['X-Content-Category'] = 'Educational'  # Категория контента
    response.headers['X-Scientific-Name'] = 'Panthera pardus'  # Научное название
    response.headers['X-Page-Generated'] = 'Flask Server'  # Информация о генерации
    
    return response

    
count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    
    clear_url = url_for('clear_counter')
    
    return f'''
<!doctype html>
<html>
    <head>
        <title>Счетчик посещений</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            a {{ color: #0066cc; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            .info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1> Счетчик посещений</h1>
        
        <div class="info">
            <strong>Сколько раз вы сюда заходили:</strong> {count}
        </div>
        
        <hr>
        
        <div>
            <strong>Дата и время:</strong> {time}<br>
            <strong>Запрошенный адрес:</strong> {url}<br>
            <strong>Ваш IP адрес:</strong> {client_ip}<br>
        </div>
        
        <hr>
        
        <a href="{clear_url}"> Очистить счетчик</a>
    </body>
</html>
'''

@app.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@app.route("/lab1/info")
def info():
    return redirect('/author')

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
<html>
''', 201


@app.errorhandler(404)
def not_found(err):
    error_page = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Страница не найдена</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                color: white;
                text-align: center;
            }
            .error-container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                max-width: 500px;
                margin: 20px;
            }
            h1 {
                font-size: 4em;
                margin: 0;
                color: #ffd700;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            h2 {
                font-size: 1.8em;
                margin: 10px 0 20px 0;
            }
            p {
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .emoji {
                font-size: 5em;
                margin: 20px 0;
                display: block;
            }
            .home-button {
                display: inline-block;
                background: #ff6b6b;
                color: white;
                padding: 12px 30px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 1.1em;
            }
            .home-button:hover {
                background: #ff5252;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
            }
            .search-icon {
                width: 100px;
                height: 100px;
                margin: 0 auto 20px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="search-icon">🔍</div>
            <h1>404</h1>
            <h2>Ой! Страница потерялась в космосе</h2>
            <p>Похоже, эта страница отправилась в незапланированное путешествие. Возможно, она сейчас любуется звездами где-то далеко-далеко...</p>
            <img src="/static/li.webp" alt="Космос" style="width: 200px; height: 120px; margin: 0 auto 20px; display: block;">
            <p>Но не расстраивайтесь! Вы можете вернуться на главную страницу и продолжить исследование нашего сайта.</p>
            <button class="home-button" onclick="window.location.href='/'">Вернуться на главную</button>
        </div>
        
        <script>
            // Добавляем немного интерактивности
            document.querySelector('.home-button').addEventListener('mouseover', function() {
                this.style.transform = 'scale(1.05)';
            });
            
            document.querySelector('.home-button').addEventListener('mouseout', function() {
                this.style.transform = 'scale(1)';
            });
        </script>
    </body>
    </html>
    """
    return error_page, 404



@app.route("/")
@app.route('/index')
def index():  
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        header {
            background-color: red;
            color: white;
            padding: 20px;
            text-align: center;
        }
        nav {
            background-color: green;
            padding: 10px;
        }
        nav a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            display: inline-block;
        }
        nav a:hover {
            background-color: #006b52;
        }
        main {
            padding: 20px;
            min-height: 400px;
        }
        footer {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            margin-top: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <nav>
            <a href="/lab1">Первая лабораторная</a>
        </nav>
        
        <main>
            <h2>Добро пожаловать на сайт лабораторных работ!</h2>
            <p>Здесь будут размещены все лабораторные работы по курсу WEB-программирование.</p>
        </main>
        
        <footer>
            Елизавета, Группа ФБИ-33, 3 курс, 2025 год
        </footer>
    </div>
</body>
</html>
'''

@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная 1</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .menu { margin: 20px 0; }
        .menu a { color: #0066cc; text-decoration: none; margin-right: 20px; }
        .menu a:hover { text-decoration: underline; }
        .text {
            font-size: 20px;
            color: #333;
            text-align: justify;
            margin: 40px 0;
            line-height: 1.6;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #0066cc;
        }
    </style>
</head>
<body>
    <h1>Первая лабораторная работа</h1>
    
    <div class="menu">
        <a href="/">Главная страница</a>
        <a href="/lab1/image">Изображение</a>
        <a href="/counter">Счетчик</a>
    </div>

    <div class="text">
        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.
    </div>
    
    <p style="text-align: center;">
        <a href="/">Вернуться на главную страницу</a>
    </p>
    
    <h2>Задания лабораторной работы:</h2>
    <ul>
        <li>Страница с изображением</li>
        <li>Страница со счетчиком посещений</li>
        <li>Подключение CSS стилей</li>
    </ul>
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
    return error_page, 500
    app.run(debug=False, host='0.0.0.0', port=5000)