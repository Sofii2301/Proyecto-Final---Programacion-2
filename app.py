from flask import Flask, session, redirect, url_for, request, jsonify
from flask import render_template
import json
app = Flask(__name__)
app.secret_key = "secreto"

#Archivos json
with open("usuarios.json", encoding='utf-8') as users:
    usuarios_data = json.load(users)
with open("peliculas.json", encoding='utf-8') as pelis:
    pelis_data = json.load(pelis)

def usuario():
    if 'user' in session:
        name = session['user']
    else:
        name = ''
    return name

def error(dato):    
    return render_template('error.html',name=usuario(),dato=dato)

#Rutas
@app.route("/",methods=["GET"])
def home():
    session['contador'] = session.get('contador',0) + 1
    contador_visitas=session['contador']
    return render_template('index.html',name=usuario(),peliculas=pelis_data,visitas=contador_visitas)

@app.route("/ingresar" )
def ingresar():
    return render_template('ingresar.html',name=usuario())

@app.route("/login", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        for i in (usuarios_data):
            if i["nombre"]==request.form["username"] and i["contrasenia"] == request.form["password"]:
                session["user"]=i["nombre"]
                return redirect(url_for("home"))
        return "Usuario o contrasenia incorrectos"   

@app.route("/directores")
def directores():
    return render_template('directores.html',name=usuario(),peliculas=pelis_data)
@app.route("/generos")
def generos():
    return render_template('generos.html',name=usuario(),peliculas=pelis_data,)
@app.route("/imagenes")
def imagenes():
    return render_template('imagenes.html',name=usuario(),peliculas=pelis_data)
@app.route("/confirmar", methods=["POST","GET"])
def confirm():
    if request.method == "POST":
        directores=request.form["directores"]
        directores=directores.title()
        for i in pelis_data:
            if i["Director"] == directores:
                return redirect(url_for("buscar_directores", director=i["Director"]))
    return error(directores)
@app.route("/buscarDirectores",methods=["POST","GET"])
def buscar_directores():
    director1 = request.args.get('director')
    return render_template('buscar_directores.html',name=usuario(), peliculas=pelis_data, director1=director1)
@app.route("/confirmar_peliculas", methods=["POST","GET"])
def confirm_peliculas():
    if request.method == "POST":
        titulo=request.form["titulo"]
        titulo=titulo.title()
        for i in pelis_data:
            if i["Titulo"] == titulo:
                return redirect(url_for("buscar_peliculas", titulo=i["Titulo"]))
    return error(titulo)
@app.route("/buscarPeliculas")
def buscar_peliculas():
    titulo1=request.args.get('titulo')
    return render_template('buscar_peliculas.html',name=usuario(),peliculas=pelis_data,titulo1=titulo1)
@app.route("/confirmar_actores", methods=["POST","GET"])
def confirm_actores():
    if request.method == "POST":
        actores=request.form["actores"]
        actores=actores.title()
        for i in pelis_data:
            if i["Actores"] == actores:
                return redirect(url_for("buscar_actores", actor=i["Actores"]))
    return error(actores)
@app.route("/buscarActores")
def buscar_actores():
    actor1=request.args.get('actor')
    return render_template('buscar_actores.html',name=usuario(),peliculas=pelis_data,actor1=actor1)
@app.route("/agregarPeli", methods=['GET', 'POST'])
def agregar():
    director=[]
    genero=[]
    if 'user' not in session: 
        return redirect(url_for('home'))
    if request.method == 'POST':
        pelicula = {
            "img": request.form['imagen'],
            "Titulo": request.form['titulo'], 
            "Director": request.form['director'], 
            "año" : request.form['anio'], 
            "Genero" : request.form['genero'],
            "Sinopsis" : request.form['sinopsis'],
            "Actores" :request.form['actores'],
            "Comentarios":[
                {
                    "Usuario":session["user"],
                    "Comentario":request.form["opinion"]
                }
            ]
        }
        
        
        pelis_data.append(pelicula)
        
    for datos in pelis_data:
        director.append(datos['Director'])
        genero.append(datos['Genero'])    
    return render_template('agregarPeli.html',name=usuario(), directores=director, generos=genero)

@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('home'))
app.run( debug=True, port=8000 )