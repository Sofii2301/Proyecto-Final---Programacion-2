from flask import Flask, session, redirect, url_for, request, jsonify
from flask import render_template
import json

app = Flask(__name__)
app.secret_key = "secreto"

#Archivos json
with open("usuarios.json", encoding='utf-8') as users:
    usuarios_data = json.load(users)

@app.route("/",methods=["GET"])
def home(nombre='perfil'):
    return render_template('index.html',name=nombre)

@app.route("/ingresar" )
def ingresar():
    return render_template('ingresar.html')

@app.route("/login", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        for i in (usuarios_data):
            if i["nombre"]==request.form["username"] and i["contrasenia"] == request.form["password"]:
                session["user"]=i["nombre"]
                return redirect(url_for("log", name=session["user"]))
        return "Usuario o contrasenia incorrectos"   
    

@app.route("/<name>")
def log(name):
    if 'user' in session:
        return render_template("logueado.html", name=name)
    else: 
        return "Necesita estar logueado"

@app.route("/directores")
def directores():
    return render_template('directores.html')

@app.route("/generos")
def generos():
    return render_template('generos.html')

@app.route("/agregarPeli")
def agregar():
    return render_template('agregarPeli.html')

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('home'))


app.run( debug=True, port=8000 )