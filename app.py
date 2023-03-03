from flask import Flask, session, redirect, url_for
from flask import render_template
app = Flask(__name__)

@app.route("/",methods=["GET"])
def home(name='perfil'):
    return render_template('index.html',name=name)

@app.route("/ingresar")
def ingresar():
    return render_template('ingresar.html')

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
  return redirect(url_for('index'))


app.run( debug=True, port=8000 )