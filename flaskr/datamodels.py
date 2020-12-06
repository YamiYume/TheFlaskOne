from datetime import date
from flaskr.exceptions import *
import firebase_admin
from firebase_admin import firestore
from datetime import datetime

class product():
    def __init__(self,ide="",productName=""):
        try:
            self.ide=int(ide)
        except ValueError:
            raise WrongDataException
        self.productName=str(productName)
    def data(self):
        return {'ide':self.ide,'productName':self.productName,'state':True}
    def kind(self):
        return 'products'

class importation():
    def __init__(self,ide="",count=""):
        try:
            self.ide=int(ide)
        except ValueError:
            raise WrongDataException
        try:
            self.count=int(count)
        except ValueError:
            raise WrongDataException
        self.state=True
        self.date=datetime.now()
        self.date=self.date.strftime("%m_%d_%Y_%H_%M_%S")
    def data(self):
        return {'ide':self.ide,'count':self.count,'state':self.state,'date':self.date}
    def kind(self):
        return 'imports'
        
class exportation():
    def __init__(self,ide="",count=""):
        try:
            self.ide=int(ide)
        except ValueError:
            raise WrongDataException
        try:
            self.count=int(count)
        except ValueError:
            raise WrongDataException
        self.state=True
        self.date=datetime.now()
        self.date=self.date.strftime("%m_%d_%Y_%H_%M_%S")
    def data(self):
        return {'ide':self.ide,'count':self.count,'state':self.state,'date':self.date}
    def kind(self):
        return 'exports'