import os
from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flaskr.exceptions import *

cred=credentials.Certificate("./ignore/theflaskone-firebase-adminsdk-ohkvk-0eb1aa23cc.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

from flaskr.firestorethings import WriterFirestore

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        A=WriterFirestore()
        fun={
            'ide':2,
            'count':10,
            'state':True,
        }
        try:
            B=A.register('products',fun)
        except RedundancyException:
            return 'Alredy Created'
        except ExistenceException:
            return 'The Product Not Exist'
        except ProcrastinatingException:
            return 'The Function Not Works'
        return 'Hello, World!'
    return app
