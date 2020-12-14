from flask import Flask

#Ceci est le nom de l'application
app = Flask(__name__)

#URL vers la page d'accueil
@app.route('/')
def index():
    return 'Hello FLASK,  this is a global Flask application instance'

