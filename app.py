from flask import Flask, url_for
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
        "</html>"""

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



@app.route("/image")
def image():
    path = url_for('static', filename='s-I1600.jpg')
    return (
        "<!doctype html>"
        "<html>"
        "   <body>"
        "       <h1>Дуб</h1>"
        f"       <img src='{path}'>"
        "   </body>"
        "</html>"
    )