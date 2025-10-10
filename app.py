from flask import Flask, url_for, request, redirect, render_template, abort, make_response,  send_file, Response, abort
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
        <img src="/static/i.webp" alt="Леопард">
        <p>Леопард (барс, пантера, лат. Panthera pardus) — вид хищных млекопитающих семейства кошачьих.</p>
        
        <div class="nav-links">
            <a href="/lab1">← Назад к лабораторной работе</a>
            <a href="/">На главную страницу →</a>
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
        <p><a href="/lab1">← Вернуться к лабораторной</a></p>
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

@app.route('/lab1')
def lab1():
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
        <a href="/">/ (Главная)</a>
        <a href="/index">/index (Альтернативная главная)</a>
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

@app.route('/lab2')
def lab2_main():
    return render_template('lab2_main.html')

@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'



flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    else:
        flower = flower_list[flower_id]
        return render_template('flower_detail.html', 
                             flower_id=flower_id, 
                             flower=flower)

@app.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price:
            flower_list.append({'name': name, 'price': int(price)})
            return redirect('/lab2/all_flowers')
        else:
            return render_template('add_flower_form.html', error="Заполните все поля")
    
    return render_template('add_flower_form.html')

@app.route('/lab2/add_flower/<name>')
def add_flower_with_name(name):
    flower_list.append({'name': name, 'price': 300}) 
    return redirect('/lab2/all_flowers')

@app.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', flower_list=flower_list)

@app.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers')

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')

@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Стабровская Лиза', 2, 'ФБИ-33',3
    fruits=[
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
        
    return render_template('example.html',
                            name=name, lab_num=lab_num,group=group,
                            course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filtres')
def filtres():
    phrase="О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/calc/')
def calc_default():
    """Перенаправление на калькулятор с значениями по умолчанию"""
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    """Перенаправление на калькулятор с одним числом и вторым по умолчанию"""
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'sum': a + b,
        'difference': a - b,
        'product': a * b,
        'quotient': a / b if b != 0 else 'Ошибка: деление на ноль',
        'power': a ** b
    }
    
    return render_template('calc.html', a=a, b=b, operations=operations)

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 320},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

cats = [
    {
        'name': 'Такса',
        'image': 'a7675d70f12e9911ea69fe9666ceae42.jpg',
        'description': 'Милая сосиска.'
    },
    {
        'name': 'Пудель',
        'image': 'cc8658fbaa3f9622235a0e3be8759a29.jpg',
        'description': 'Белое облачко.'
    },
    {
        'name': 'Хаски',
        'image': '59cd46c3fa80363b2267f9b142b21301.jpg',
        'description': 'Разные глазки.'
    },
    {
        'name': 'Немецкая овчарка',
        'image': '2dc3c030431710c0eccf56c376376c2f.jpg',
        'description': 'Серьезная собака.'
    },
    {
        'name': 'Алабай',
        'image': '1f83db3c6aa33be78e996d717ec7ac2e.jpg',
        'description': 'Не люблю эту породу, покусали в детстве.'
    },
    {
        'name': 'Доберман',
        'image': '6766da6bba7e9db14e6d94e873276e6d.jpg',
        'description': 'Зверь, а не собака.'
    },
    {
        'name': 'Сиба-ину',
        'image': '5864bbc3fb2a2034a0c619d82427d31e.jpg',
        'description': 'Плачу как впервый раз, смотря "Хатико".'
    },
    {
        'name': 'Бульдог',
        'image': '0e80503c2a88ad187c1777875086ce74.jpg',
        'description': 'Похож на милую свинку.'
    },
    {
        'name': 'Шпиц',
        'image': '420ae034ee040ce2a5232e6cf845453b.jpg',
        'description': 'Собака истинных леди.'
    },
    {
        'name': 'Бишон фризе',
        'image': '8847d87ad716fcd9f8440ecdfccae916.jpg',
        'description': 'У меня моя краостка такой породы.'
    },
    {
        'name': 'Бобтейл',
        'image': '0011c5dd8b82085fcfcf2773da9e98ed.jpg',
        'description': 'Обладатель самой длинной челки.'
    },
    {
        'name': 'Спаниель',
        'image': '63a0d555b2dc45b7f200ef303ee44870.jpg',
        'description': 'Кудряшка Сью.'
    },
    {
        'name': 'Бирманский',
        'image': '5f5ac46a1738e48ca1c086e67fd52b3e.jpg',
        'description': 'Полудлинношёрстный кот с белыми "носочками" и голубыми глазами.'
    },
    {
        'name': 'Турецкий ван',
        'image': '4493397b1c48dfa5af562a9263bf2b74.jpg',
        'description': 'Порода, которая любит воду и имеет характерный красно-белый окрас.'
    },
    {
        'name': 'Египетский мау',
        'image': 'c66fa40e31beb6ff86abd5bce1cf5e71.jpg',
        'description': 'Единственная естественная порода с пятнистым окрасом.'
    },
    {
        'name': 'Тонкинский',
        'image': '8ee07b304e6dcfa26adea336bb50eefa.jpg',
        'description': 'Гибрид сиамской и бурманской пород с аквамариновыми глазами.'
    },
    {
        'name': 'Корат',
        'image': 'e1d36188aa88cba858b5e26b12072338.jpg',
        'description': 'Древняя порода из Таиланда с серебристо-голубой шерстью.'
    },
    {
        'name': 'Манчкин',
        'image': 'static/on.jpg',  # <- Исправлено: закрыты кавычки и добавлено расширение
        'description': 'Порода с короткими лапами и игривым характером.'
    },
    {
        'name': 'Девон-рекс',
        'image': 'd0d1069a1148c58fdf930a3f3f8f37d4.jpg',
        'description': 'Кот с волнистой шерстью, большими ушами и озорным характером.'
    },
    {
        'name': 'Сибирский',
        'image': 'acee46c88e8b3dad7dee4673204f97da.jpg',
        'description': 'Русская порода с густой шерстью и гипоаллергенными свойствами.'
    }  
]
@app.route('/lab2/catsanddog')
def cats_gallery():
    return render_template('catsanddog.html', cats=cats)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)