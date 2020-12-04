from flaskr import db
import google.cloud
import firebase_admin
from firebase_admin import firestore

class WriterFirestore():
    def __init__(self):
        pass
    def register(self,kind,data):
        if kind=='product':
            self.docR = db.collection('products').document(str(data['ide']))
            self.doc = self.docR.get()
            if not(self.doc.exists):
                db.collection("products").document(str(data['ide'])).set(data)
            else:
                raise ValueError
        elif kind=='import':
            self.docR = db.collection(u'products').document(str(data['ide']))
            self.doc = self.docR.get()
            if not(self.doc.exists):
                raise ValueError
            else:
                try:
                    self.Count=SearcherFirestoredev(data['ide'],'imports')
                except ValueError:
                    db.collection("imports").document(str(data['ide'])).set(data)
                    return(3345)
                else:
                    db.collection("imports").document(str(data['ide'])+str(self.Count.l())).set(data)
                    return (self.Count.l())
        elif kind=='export':
            self.docR = db.collection(u'products').document(str(data['ide']))
            self.doc = self.docR.get()
            if not(self.doc.exists):
                raise ValueError
            else:
                try:
                    self.Count=SearcherFirestoredev(data['ide'],'exports')
                except ValueError:
                    db.collection("exports").document(str(data['ide'])).set(data)
                    return(3345)
                else:
                    db.collection("exports").document(str(data['ide'])+str(self.Count.l())).set(data)
                    return (self.Count.l())
        else:
            raise ReferenceError

class SearcherFirestoredev:
    def __init__(self,ide,kind):
        if kind=='products':
            self.ide=ide
            self.query=db.collection('products').where('ide','==',self.ide).get()
            self.counter=0
            for doc in self.query:
                self.counter=self.counter+1
            if self.counter==0:
                raise ValueError
        elif kind=='imports':
            self.ide=int(ide)
            self.query=db.collection('imports').where(u"ide",'==',self.ide).get()
            self.counter=0
            for doc in self.query:
                self.counter=self.counter+1
            if self.counter is 0:
                raise ValueError
        elif kind=='exports':
            self.ide=int(ide)
            self.query=db.collection('exports').where(u"ide",'==',self.ide).get()
            self.counter=0
            for doc in self.query:
                self.counter=self.counter+1
            if self.counter is 0:
                raise ValueError
    def get(self):
        return self.query
    def l(self):
        self.counter=0
        for doc in self.query:
            self.counter=self.counter+1
        return self.counter