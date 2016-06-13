# -*- coding: utf-8 -*-
from flask import Flask,render_template, request, send_from_directory
from flask.ext.script import Manager
from os import path

#déclare le serveur flask
app = Flask(__name__)

#déclare le plug-in flask-script
manager = Manager(app)

#crée la route web de la racine du site
#et la lie à la fonction index
@app.route("/")
def index():
    return "ceci est la page index"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/groundtruth/<path:path>')
def send_groundtruth(path):
    return send_from_directory('groundtruth', path)

#on crée la nouvelle route et on la lie à fonction Hello
@app.route('/stif')
@app.route('/stif/<name>')
def hello(name=None):
    if name == None :
        fName = 'static/index.html'
        name = 'index.html'
    else:
    	fName = "static/"+name
    if not path.isfile(fName):
    	return "HTTP error 404 : file not found"
    else:
       	return app.send_static_file(name)

if __name__ == "__main__":
    #lance le serveur Flask via le plug-in flask-script
    manager.run()
