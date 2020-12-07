from flaskr.exceptions import *
from flask import (Blueprint, flash, render_template, request,redirect)
from flaskr.datamodels import exportation
from flaskr.firestorethings import (WriterFirestore,historyFirestore,deleter,SearcherFirestoredev)

bp = Blueprint('exportspages', __name__, url_prefix='/exportspages')

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
                exportdata=exportation(ide,count)
            except WrongDataException:
                error='Wrong data'
            else:
                exportregister=WriterFirestore()
                try:
                    exportregister.register( exportdata.kind(), exportdata.data())
                except ExistenceException:
                    error='trying to register an export of a non-existent product'
                except WrongDataException:
                    error='trying to export more than total count'
        if not(error is None):
            flash(error)
    return render_template('exportspages/add.html')
@bp.route('/history',methods=('GET', 'POST'))
def history():
    if request.method=='POST':
        ide=request.form['ide']
        if not ide:
            error='ide required'
        else:
            datahistory=historyFirestore('exports',ide)
            datahistory=datahistory.data()
            return render_template('exportspages/history.html',datahistory=datahistory)
    else:
        datahistory=historyFirestore('exports')
        datahistory=datahistory.data()  
    return render_template('exportspages/history.html',datahistory=datahistory)
@bp.route('/delt/<string:ide>',methods=('POST',))
def delt(ide):
    delet=deleter(ide,'exports')
    delet.trsh()
    return redirect('/exportspages/history')