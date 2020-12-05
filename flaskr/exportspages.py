from flaskr.exceptions import *
from flask import (Blueprint, flash, render_template, request,)
from flaskr.datamodels import exportation
from flaskr.firestorethings import WriterFirestore

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
        if not(error is None):
            flash(error)
    return render_template('exportspages/add.html')