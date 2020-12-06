from flaskr.exceptions import *
from flask import (Blueprint, flash, render_template, request,redirect)
from flaskr.datamodels import importation
from flaskr.firestorethings import (WriterFirestore,historyFirestore,deleter)

bp = Blueprint('importspages', __name__, url_prefix='/importspages')

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method=='POST':
        ide=request.form['ide']
        count=request.form['count']
        error=None
        if not ide:
            error='ide required'
        elif not count:
            error='count required'
        else:
            try:
                importdata=importation(ide,count)
            except WrongDataException:
                error='Wrong data'
            else:
                importregister=WriterFirestore()
                try:
                    importregister.register(importdata.kind(),importdata.data())
                except ExistenceException:
                    error='trying to register an import of a non-existent product'
        if not(error is None):
            flash(error)
    return render_template('importspages/add.html')
@bp.route('/history',methods=('GET', 'POST'))
def history():
    datahistory=historyFirestore('imports')
    datahistory=datahistory.data()  
    return render_template('importspages/history.html',datahistory=datahistory)
@bp.route('/delt/<string:ide>',methods=('POST',))
def delt(ide):
    delet=deleter(ide,'imports')
    delet.trsh()
    return redirect('/importspages/history')