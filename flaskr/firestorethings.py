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
        elif self.kind=='imports':
            try:
                self.exist=SearcherFirestoredev(data['ide'],'products')
            except ExistenceException:
                raise ExistenceException
            else:
                db.collection(kind).add(data)
        elif self.kind=='exports':
            try:
                self.exist=SearcherFirestoredev(data['ide'],'products')
            except ExistenceException:
                raise ExistenceException
            else:
                try:
                    A=SearcherFirestoredev(data['ide'],'imports')
                except ExistenceException:
                    try:
                        B=SearcherFirestoredev(data['ide'],'exports')
                    except ExistenceException:
                        self.total=0
                    else:
                        self.total=-B.total
                else:
                    try:
                        B=SearcherFirestoredev(data['ide'],'exports')
                    except ExistenceException:
                        self.total=A.total
                    else:
                        self.total=A-B
                if self.total>=data['count']:
                    db.collection(kind).add(data)
                else:
                    raise WrongDataException
        else:
            raise ProcrastinatingException

class SearcherFirestoredev:
    def __init__(self,ide,kind):
        self.ide=int(ide)
        self.query=db.collection(kind).where('ide','==',self.ide).get()
        self.counter=0
        self.total=0
        for doc in self.query:
            self.counter=self.counter+1
            try:
                self.total=self.total+(doc.to_dict()['count'])
            except KeyError:
                pass
        if self.counter==0:
            raise ExistenceException
    def __sub__(self,other):
        return self.total-other.total

class historyFirestore:
    def __init__(self,kind,ide=0):
        self.query=db.collection(kind).get()
        self.results=[]
        self.kind=kind
        self.ide=int(ide)
        for doc in self.query:
            self.doc=doc.to_dict()
            if self.doc and self.doc['state']:
                if not kind=='products':
                    self.squery=db.collection('products').where('ide','==',self.doc['ide']).get()
                    for sdoc in self.squery:
                        self.sdoc=sdoc.to_dict()
                        self.doc['productName']=self.sdoc['productName']
                else:
                    try:
                        A=SearcherFirestoredev(self.doc['ide'],'imports')
                    except ExistenceException:
                        try:
                            B=SearcherFirestoredev(self.doc['ide'],'exports')
                        except ExistenceException:
                            self.doc['total']=0
                        else:
                            self.doc['total']=-B.total
                    else:
                        try:
                            B=SearcherFirestoredev(self.doc['ide'],'exports')
                        except ExistenceException:
                            self.doc['total']=A.total
                        else:
                            self.doc['total']=A-B
                if self.ide:
                    if self.doc['ide']==self.ide:
                        self.results.append(self.doc)
                else:
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
                