from flask import Flask
app = Flask(__name__)

@app.route("/")
def start():
    return """<! doctype html>" 
        "<html>"
        "   <body>"  
        "       <h1>web-сервер на flask</hl>" 
        "   </body>" 
        "</html>"""


