import os
from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flaskr.exceptions import *

# to run the app:
# Download
# open the cd
# execute $venv\Scripts\activate
# execute $set FLASK_APP=flaskr
# execute $set FLASK_ENV=development
# execute $flask run
#copy url
#add /productspages/add

cred=credentials.Certificate("./ignore/theflaskone-firebase-adminsdk-ohkvk-0eb1aa23cc.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import productspages
    app.register_blueprint(productspages.bp)
    from . import exportspages
    app.register_blueprint(exportspages.bp)
    from . import importspages
    app.register_blueprint(importspages.bp)
    
    @app.route('/index')
    def hello():
        return 'Hello, World!'
    return app
