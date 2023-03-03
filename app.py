from flask import Flask
from flask import render_template
app = Flask(__name__)

usuarios=[
    {
        "id" : "8",
        "nombre" : "bruno"
    },
    {
        "id" : "20",
        "nombre" : "emanuel"
    },
    {
        "id" : "10",
        "nombre" : "sofi",
    }
]
@app.route ("/")
def index():
    return "hola server"
@app.route("/home")
def home(name='perfil'):
    return render_template('index.html',name=name)
@app.route("/login")
def login():
    return render_template('login.html')
app.run( debug=True, port=8000 )