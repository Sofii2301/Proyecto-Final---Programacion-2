from flask import Flask, session, redirect, url_for, request, jsonify
from flask import render_template
import json
app = Flask(__name__)
app.secret_key = "secreto"
#Archivos json
with open("usuarios.json", encoding='utf-8') as users:
    usuarios_data = json.load(users)
#archivos peliculas
with open("peliculas.json", encoding='utf-8') as pelis:
    pelis_data = json.load(pelis)
@app.route("/",methods=["GET"])
def home(nombre=''):
    session['contador'] = session.get('contador',0) + 1
    contador_visitas=session['contador']
    return render_template('index.html',name=nombre,peliculas=pelis_data,visitas=contador_visitas)

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
    return render_template('directores.html',peliculas=pelis_data)
@app.route("/generos")
def generos():
    return render_template('generos.html',peliculas=pelis_data,)
@app.route("/imagenes")
def imagenes():
    return render_template('imagenes.html',peliculas=pelis_data)
@app.route("/confirmar", methods=["POST","GET"])
def confirm():
    if request.method == "POST":
         for i in pelis_data:
            if i["Director"] == request.form["directores"]:
                return redirect(url_for("buscar_directores", director=i["Director"]))
    return "no se encontraron directores" 
@app.route("/buscarDirectores",methods=["POST","GET"])
def buscar_directores():
    director1 = request.args.get('director')
    return render_template('buscar_directores.html', peliculas=pelis_data, director1=director1)
@app.route("/confirmar_peliculas", methods=["POST","GET"])
def confirm_peliculas():
    if request.method == "POST":
         for i in pelis_data:
            if i["Titulo"] == request.form["titulo"]:
                return redirect(url_for("buscar_peliculas", titulo=i["Titulo"]))
    return "no se encontro el titulo" 
@app.route("/buscarPeliculas")
def buscar_peliculas():
    titulo1=request.args.get('titulo')
    return render_template('buscar_peliculas.html',peliculas=pelis_data,titulo1=titulo1)
@app.route("/confirmar_actores", methods=["POST","GET"])
def confirm_actores():
    if request.method == "POST":
         for i in pelis_data:
            if i["Actores"] == request.form["actores"]:
                return redirect(url_for("buscar_actores", actor=i["Actores"]))
    return "no se encontro al actor"
@app.route("/buscarActores")
def buscar_actores():
    actor1=request.args.get('actor')
    return render_template('buscar_actores.html',peliculas=pelis_data,actor1=actor1)
@app.route("/agregarPeli")
def agregar():
    return render_template('agregarPeli.html')
@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('home'))
app.run( debug=True, port=8000 )