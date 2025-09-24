from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/web")
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


@app.route("/author")
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

@app.route('/counter')
def counter():
    global count
    count +=1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + str(client_ip) + '''<br>
    </body>
</html>
'''
@app.route("/info")
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
