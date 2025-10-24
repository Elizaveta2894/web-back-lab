from flask import Blueprint, url_for, redirect
lab1= Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/image')
def image():
    css_url = url_for('static', filename='lab1/lab1.css')
    
    html_content = f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="{css_url}">
    <title>Леопард - Лабораторная 1</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 30px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #2d3436;
            text-align: center;
            margin-bottom: 30px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            display: block;
            margin: 0 auto 20px;
        }}
        p {{
            font-size: 18px;
            line-height: 1.6;
            color: #2d3436;
            text-align: center;
            background: #dfe6e9;
            padding: 20px;
            border-radius: 8px;
        }}
        .nav-links {{
            text-align: center;
            margin-top: 30px;
        }}
        .nav-links a {{
            display: inline-block;
            margin: 0 10px;
            padding: 12px 25px;
            background: #00b894;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.3s ease;
        }}
        .nav-links a:hover {{
            background: #00a085;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Леопард</h1>
        <img src="lab1/i.webp" alt="Леопард">
        <p>Леопард (барс, пантера, лат. Panthera pardus) — вид хищных млекопитающих семейства кошачьих.</p>
        
        <div class="nav-links">
            <a href="/lab1">← Назад к лабораторной работе</a>
            <a href="/index">На главную страницу →</a>
        </div>
    </div>
</body>
</html>
'''
    
    from flask import make_response
    response = make_response(html_content)
    response.headers['Content-Language'] = 'ru'
    response.headers['X-Animal-Type'] = 'Big Cat'
    response.headers['X-Page-Theme'] = 'Wildlife'
    
    return response

    
count = 0


@lab1.route('/lab1/counter')
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
        <p><a href="/lab1">← Вернуться к лабораторной</a></p>
    </body>
</html>
'''


@lab1.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@lab1.route("/lab1/info")
def info():
    return redirect('/author')


@lab1.route("/lab1/created")
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


@lab1.route('/lab1')
def lab():
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Лаб 1</title>
    <style>
        body { font-family: Arial; max-width: 1000px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        h2 { color: #666; margin-top: 30px; }
        .menu a { display: inline-block; margin: 5px; padding: 10px; 
                  background: #28a745; color: white; text-decoration: none; 
                  border-radius: 3px; }
        .routes { background: #f8f9fa; padding: 20px; border-radius: 5px; }
        .routes a { display: block; padding: 8px; margin: 5px 0; 
                    background: white; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <h1>Лабораторная работа 1</h1>
    
    <div class="menu">
        <a href="/">Главная</a>
        <a href="/index">Index</a>
        <a href="/lab1/image">Изображение</a>
        <a href="/counter">Счетчик</a>
        <a href="/error500">Ошибка 500</a>
    </div>

    <p>Flask — микрофреймворк для веб-приложений на Python.</p>
    
    <h2>Список роутов</h2>
    <div class="routes">
        <a href="/index">/index (главная)</a>
        <a href="/lab1">/lab1 (Эта страница)</a>
        <a href="/lab1/image">/lab1/image (Изображение леопарда)</a>
        <a href="/counter">/counter (Счетчик посещений)</a>
        <a href="/error500">/error500 (Тест ошибки сервера)</a>
        <a href="/nonexistent">/nonexistent (Тест 404 ошибки)</a>
    </div>
</body>
</html>
'''
    return html

