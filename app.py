from flask import Flask, url_for, request, redirect
import datetime
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
    return f'''
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
    return "нет такой страницы", 404

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
