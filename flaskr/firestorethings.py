from flaskr import db
from flaskr.exceptions import *
from flaskr.datamodels import *
import datetime


class WriterFirestore():
    def __init__(self):
        pass
    def register(self,kind,data):
        self.kind=kind
        if self.kind=='products':
            try:
                self.exist=SearcherFirestoredev(data['ide'],'products')
            except ExistenceException:
                db.collection(kind).add(data)
            else:
                raise RedundancyException
        elif self.kind=='imports' or self.kind=='exports':
            try:
                self.exist=SearcherFirestoredev(data['ide'],'products')
            except ExistenceException:
                raise ExistenceException
            else:
                db.collection(kind).add(data)
        else:
            raise ProcrastinatingException

class SearcherFirestoredev:
    def __init__(self,ide,kind):
        self.ide=int(ide)
        self.query=db.collection(kind).where('ide','==',self.ide).get()
        self.counter=0
        for doc in self.query:
            self.counter=self.counter+1
        if self.counter==0:
            raise ExistenceException

class historyFirestore:
    def __init__(self,kind):
        self.query=db.collection(kind).get()
        self.results=[]
        self.kind=kind
        for doc in self.query:
            self.doc=doc.to_dict()
            if self.doc and self.doc['state']:
                if not kind=='products':
                    self.squery=db.collection('products').where('ide','==',self.doc['ide']).get()
                    for sdoc in self.squery:
                        self.sdoc=sdoc.to_dict()
                        self.doc['productName']=self.sdoc['productName']
                self.results.append(self.doc)
    def data(self):
        return self.results

class deleter:
    def __init__(self,ide,kind):
        self.ide=ide
        self.kind=kind
    def trsh(self):
        if self.kind=='products':
            self.docs=db.collection(self.kind).where('ide','==',self.ide).get()
            for doc in self.docs:
                self.doc=doc.id
                self.data=doc.to_dict()
                self.data['state']=False
                db.collection(self.kind).document(self.doc).set(self.data)
        else:
            self.docs=db.collection(self.kind).where('date','==',self.ide).get()
            for doc in self.docs:
                self.doc=doc.id
                self.data=doc.to_dict()
                self.data['state']=False
                db.collection(self.kind).document(self.doc).set(self.data)
                