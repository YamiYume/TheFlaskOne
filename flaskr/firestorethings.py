from flaskr import db
from flaskr.exceptions import *

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