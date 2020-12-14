import os
from flask import Flask

def create_app(test_config=None):
    "Application factory function"

    #create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite' ), )
    
    if test_config is None:
        #load the instance config, if it exists when not testing
         app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #simple web page that says hello
    @app.route('/visual')
    def hello():
        return 'hello to VISUAL WORLD'

    from . import db

    #Now that init-db has been registered with the app
    db.init_app(app)

    #Import and register the blueprint from the factory
    from . import auth
    app.register_blueprint(auth.bp)

    return app
        
