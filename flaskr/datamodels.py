from datetime import date
from flaskr.exceptions import *

class product():
    def __init__(self,ide="",productName=""):
        try:
            self.ide=int(ide)
        except ValueError:
            raise WrongDataException
        self.productName=str(productName)
    def data(self):
        return {'ide':self.ide,'productName':self.productName}
    def kind(self):
        return 'products'
    def retake(self,datadict):
        self.ide=datadict['ide']
        try:
            self.productName=datadict['productName']
        except KeyError:
            raise WrongDataException

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
        self.date=date.today()
    def data(self):
        return {'ide':self.ide,'count':self.count,'state':self.state,'date':self.date}
    def kind(self):
        return 'imports'
    def retake(self,datadict):
        self.ide=datadict['ide']
        try:
            self.count=datadict['count']
        except KeyError:
            raise WrongDataException
        try:
            self.state=datadict['state']
        except KeyError:
            raise WrongDataException
        try:
            self.date=datadict['date']
        except KeyError:
            raise WrongDataException
        
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
        self.date=date.today()
    def data(self):
        return {'ide':self.ide,'count':self.count,'state':self.state,'date':self.date}
    def kind(self):
        return 'exports'
    def retake(self,datadict):
        self.ide=datadict['ide']
        try:
            self.count=datadict['count']
        except KeyError:
            raise WrongDataException
        try:
            self.state=datadict['state']
        except KeyError:
            raise WrongDataException
        try:
            self.date=datadict['date']
        except KeyError:
            raise WrongDataException