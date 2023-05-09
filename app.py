import math
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
#ruta para ver el nombre del usuario
def usuario():
    if 'user' in session:
        name = session['user']
    else:
        name = ''
    return name

#ruta de error
def error(dato):    
    return render_template('error.html',name=usuario(),dato=dato)
def error2(dato):
    return render_template('error2.html',name=usuario(),dato=dato)

#Rutas
@app.route("/",methods=["GET"])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    peliculas2=pelis_data
    peliculas2=list(peliculas2)
    if len(peliculas2)>1:
        peliculas2.reverse()
    peliculas = peliculas2[start_index:end_index]
    total_peliculas = len(pelis_data)
    total_pages = math.ceil(total_peliculas / per_page)
    session['contador'] = session.get('contador',0) + 1
    contador_visitas=session['contador']
    return render_template('index.html',name=usuario(),peliculas=peliculas,visitas=contador_visitas,total_pages=total_pages, current_page=page)

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
        return render_template("errorUsuario.html", name=usuario())  

@app.route("/directores")
def directores():
    return render_template('directores.html',name=usuario(),peliculas=pelis_data)
@app.route("/generos")
def generos():
    lista=[]
    for x in pelis_data:
        if x["Genero"] not in lista:
            lista.append(x["Genero"])
    return render_template('generos.html',name=usuario(),peliculas=lista,)
@app.route("/imagenes")
def imagenes():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    peliculas = pelis_data[start_index:end_index]
    total_peliculas = len(pelis_data)
    total_pages = math.ceil(total_peliculas / per_page)
    return render_template('imagenes.html',name=usuario(),peliculas=peliculas,total_pages=total_pages, current_page=page)

#confirmar para buscar directores
@app.route("/confirmar", methods=["POST","GET"])
def confirm():
    if request.method == "POST":
        directores=request.form["directores"]
        directores=directores.title()
        lista=[]
        for i in pelis_data:
            if directores in i["Director"]:
                lista.append(i["Director"])
        if lista != "":
            director=""
            for i in lista:
                director = i + director
        return redirect(url_for("buscar_directores", director=director))
@app.route("/buscarDirectores",methods=["POST","GET"])
def buscar_directores():
    director1 = request.args.get('director')
    if director1 == None:
        director1=""
    return render_template('buscar_directores.html',name=usuario(), peliculas=pelis_data, director1=director1)

#confirmar para buscar peliculas
@app.route("/confirmar_peliculas", methods=["POST","GET"])
def confirm_peliculas():
    if request.method == "POST":
        titulo=request.form["titulo"]
        titulo=titulo.title()
        lista=[]
        for i in pelis_data:
            if titulo in i["Titulo"]:
                lista.append(i["Titulo"])
        if lista != "":
                titulo=""
                for i in lista:
                    titulo=i + titulo
                return redirect(url_for("buscar_peliculas", titulo=titulo))
    return error(titulo)
@app.route("/buscarPeliculas", methods=["POST","GET"])
def buscar_peliculas():
    titulo1=request.args.get('titulo')
    if titulo1 == None:
        titulo1=""
    return render_template('buscar_peliculas.html',name=usuario(),peliculas=pelis_data,titulo1=titulo1)

#confirmar para buscar actores
@app.route("/confirmar_actores", methods=["POST","GET"])
def confirm_actores():
    if request.method == "POST":
        actores=request.form["actores"]
        actores=actores.title()
        lista=[]
        for i in pelis_data:
            if actores in i["Actores"]:
                lista.append(i["Actores"])
        if lista != "":
                actor=","
                for i in lista:
                    actor=i + actor
                return redirect(url_for("buscar_actores", actor=actor))
@app.route("/buscarActores")
def buscar_actores():
    actor1=request.args.get('actor')
    if actor1 == None:
        actor1=""
    return render_template('buscar_actores.html',name=usuario(),peliculas=pelis_data,actor1=actor1)

#confirmar para agregar pelicula
@app.route("/confirmar_agregar", methods=['GET','POST'])
def confirm_agregar():
    if request.method == "POST":
        titulo=request.form["titulo"]
        titulo=titulo.title()
        sinopsis=request.form["sinopsis"]
        director=request.form["director"]
        año=request.form["anio"]
        genero=request.form["genero"]
        actores=request.form["actores"]
        actores=actores.title()
        imagen=request.form['imagen']
        comentario=request.form["opinion"]
        puntuacion=request.form["puntuacion"]
        for i in pelis_data:
            if i["Titulo"] == titulo:
                return error2(dato=i["Titulo"])
        confirmacion="S"
        return redirect(url_for('agregar',titulo=titulo,director=director,año=año,genero=genero,
                                sinopsis=sinopsis,actores=actores,confirmacion=confirmacion,imagen=imagen,
                                comentario=comentario,puntuacion=puntuacion
                                ))
@app.route("/agregarPeli", methods=['GET', 'POST'])
def agregar():
    peli_agregar=request.args.get("confirmacion")
    titulo=request.args.get("titulo")
    director1=request.args.get("director")
    año=request.args.get("año")
    genero1=request.args.get("genero")
    sinopsis=request.args.get("sinopsis")
    actores=request.args.get("actores")
    imagen=request.args.get("imagen")
    comentario=request.args.get("comentario")
    puntuacion=request.args.get("puntuacion")
    director=[]
    genero=[]
    if 'user' not in session: 
        return redirect(url_for('home'))
    if peli_agregar == 'S':
        pelicula = {
            "img":  imagen,
            "Titulo": titulo, 
            "Director": director1, 
            "año" : año, 
            "Genero" : genero1,
            "Sinopsis" :sinopsis,
            "Actores" : actores,
            "Puntuacion usuarios":"",
            "Puntuacion":puntuacion,
            "Comentarios":comentario
        }

        pelis_data.append(pelicula)
        
    for datos in pelis_data:
        director.append(datos['Director'])
        genero.append(datos['Genero'])    
    return render_template('agregarPeli.html',name=usuario(), directores=director, generos=genero)

#rutas para usuario
@app.route("/crear_usuario", methods=["GET","POST"])
def crear_usuario():
    if request.method == "POST":
        for i in (usuarios_data):
            if i["nombre"]==request.form["username"]:
                return error2(dato=i["nombre"])
        nuevo_usuario = {
                "id" : "6",
                "nombre": request.form["username"],
                "contrasenia": request.form["password"]
            }
        usuarios_data.append(nuevo_usuario)
        return redirect (url_for("home"))
    return render_template("crearUsuario.html",name=usuario())
@app.route("/eliminar_usuario",methods=["GET","POST"])
def eliminar_usuario():
    if request.method == "POST":
        for i in (usuarios_data):
            if i["nombre"]==request.form["username"]:
                usuarios_data.remove(i)
                return redirect(url_for("logout"))
    return render_template('eliminar_usuario.html',name=usuario())
@app.route("/modificar_usuario",methods=["GET","POST"])
def modificar_usuario():
    if request.method == "POST":
        for i in (usuarios_data):
            if request.form["new_username"] != "":
                print (i["contrasenia"])
                if i["nombre"]==request.form["username"] and i["contrasenia"] == request.form["password"]:
                    i["nombre"]=request.form["new_username"]
                    i["contrasenia"]=request.form["new_password"]
                    return redirect(url_for("home"))
            else:
                if request.form["new_password"] != "":
                    if i["nombre"]==request.form["username"]:
                        i["contrasenia"]==request.form["new_password"]
    return render_template('editar_usuario.html',name=usuario())

#ruta para peliculas
@app.route('/eliminar/<peli>', methods=["GET","POST"])
def eliminarPeli(peli):
    if 'user' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            for pelicula in pelis_data:
                if pelicula['Titulo']==peli:
                    pelis_data.remove(pelicula)
            return redirect(url_for('home'))
    return render_template('eliminarPeli.html',name=usuario(), peli=peli)
@app.route('/editar/<peli>', methods=["GET","POST"])
def editarPeli(peli):
    if 'user' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            for pelicula in pelis_data:
                if pelicula['Titulo']==peli:
                    if request.form.get('titulo') != "":
                        pelicula['Titulo']=request.form.get('titulo')
                    if request.form.get("imagen") != "":
                        pelicula['img']=request.form.get("imagen")
                    if request.form.get("anio") != "":
                        pelicula['año']=request.form.get("anio")
                    if request.form.get("sinopsis") != "":
                        pelicula['Sinopsis']=request.form.get("sinopsis")
                    if request.form["director"] != "":
                        pelicula["Director"]=request.form.get("director")
                    if request.form["genero"] != "":
                        pelicula["Genero"] = request.form.get("genero")
                    if request.form["comentario"] != "":
                        comentario=request.form.get("comentario")
                        comentarios= pelicula["Comentarios"]
                        if type (comentario) == str:
                            comentarios= comentarios.split(',')
                        user=",usuario "
                        name=usuario()
                        user=user+name
                        user=user+":"
                        comentarios.append(user)
                        comentarios.append(comentario)
                        string="".join(comentarios)
                        pelicula["Comentarios"]=string

    return render_template('editarPeli.html',name=usuario(), peli=peli)

#buscador de peliculas por director en director
@app.route('/peliculas/<director>', methods=["GET","POST"])
def pelisDire(director):
    peliculas = []
    if request.method == "POST":
        for pelicula in pelis_data:
            if pelicula['Director']==director:
                peliculas.append(pelicula)
    return render_template("pelisDire.html",name=usuario(), director=director, peliculas=pelis_data)

#ruta para puntuar una peli
@app.route('/puntuar/<peli>',methods=["GET","POST"])
def modificarPuntuacion(peli):
    if 'user' not in session:
        return redirect(url_for('index'))
    else:
        if request.method=="POST":
            contador=2
            for pelicula in pelis_data:
                if pelicula["Titulo"]==peli:
                    esta=False
                    if pelicula["Puntuacion usuarios"] != "":
                        contador=1
                        comentario=pelicula["Puntuacion usuarios"]
                        comentario=comentario.split(",")
                        lista=[]
                        lista2=[]
                        for x in comentario:
                            lista2.append(x)
                        for usuario1 in usuarios_data:
                            for i in comentario:
                                if i == usuario1["nombre"]:
                                    lista.append(i)
                        for i in lista:
                            contador=contador+1
                        for x in comentario:
                            if x == usuario():
                                esta=True
                                cambiar=x
                                cambiar=cambiar+","+request.form["puntuacion"]
                                lista2.remove(x)
                                continue
                            if esta == True:
                                lista2.remove(x)
                                resultado2=""
                                for z in lista2:
                                    resultado2=resultado2+","+str(z)
                                resultado2=resultado2+","+cambiar
                                pelicula["Puntuacion usuarios"]=resultado2
                                break
                    if request.form["puntuacion"] != "":
                        puntuacion=pelicula["Puntuacion"]
                        puntuacion2=request.form["puntuacion"]
                        puntuacion=int (puntuacion)
                        puntuacion2=int (puntuacion2)
                        puntuacion=puntuacion+puntuacion2
                        puntuacion=puntuacion/contador
                        pelicula["Puntuacion"]=puntuacion
                        if esta == False:
                            usuario2=usuario()
                            puntuacion2=str(puntuacion2)
                            combinado=usuario2+","+puntuacion2
                            resultado=pelicula["Puntuacion usuarios"]
                            resultado=resultado+","+combinado
                            pelicula["Puntuacion usuarios"]=resultado
                                
    return render_template("puntuarPeli.html",name=usuario(),peli=peli)

#ruta para eliminar una puntuacion
@app.route('/puntuar/eliminar/<peli>',methods=["GET","POST"])
def eliminarPuntuacion(peli):
    if request.method=="POST":
        for pelicula in pelis_data:
            if pelicula["Titulo"]==peli:
                esta=False  
                if pelicula["Puntuacion usuarios"] != "":
                    contador=0
                    comentario=pelicula["Puntuacion usuarios"]
                    comentario=comentario.split(",")
                    lista2=[]
                    for x in comentario:
                        lista2.append(x)
                    for z in range(len(lista2)):
                        if lista2[z] == usuario():
                            lista2.pop(z)
                            esta=True
                            if esta == True:
                                lista2.pop(z)
                                break
                    resultado=""
                    nota=0
                    for x in lista2:
                        if x.isdigit():
                            numero=int(x)
                            contador=contador+1
                            nota=nota+numero
                        resultado=resultado+","+str(x)
                    nota=nota/contador
                    pelicula["Puntuacion"]=nota
                    pelicula["Puntuacion usuarios"]=resultado
                    return redirect(url_for("home"))
                else:
                    return error(dato="Puntuacion")
    return render_template("puntuarPeli.html",name=usuario(),peli=peli)


#ruta para modificar director
@app.route('/modificar_director',methods=["GET","POST"])
def modificar_director():
    if request.method == "POST":
        for i in pelis_data:
            if request.form["director"]==i["Director"]:
                i["Director"] =request.form["new_director"]
        return redirect(url_for('home'))
    return render_template('modificar_director.html',name=usuario(),peliculas=pelis_data)
#ruta para modificar genero
@app.route('/modificar_generos',methods=["GET","POST"])
def modificar_genero():
    lista=[]
    for x in pelis_data:
        if x["Genero"] not in lista:
            lista.append(x["Genero"])
    if request.method == "POST":
        for i in pelis_data:
            if request.form["genero"] in i["Genero"]:
                i["Genero"] =request.form["new_genero"]
        return redirect(url_for('home'))
    return render_template('modificar_generos.html',name=usuario(),peliculas=lista)
#ruta para cerrar sesion
@app.route('/logout')
def logout():
  session.pop('user', None)
  return redirect(url_for('home'))
app.run( debug=True, port=8000 )