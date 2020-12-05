from flaskr.exceptions import *
from flask import (Blueprint, flash, render_template, request,)
from flaskr.datamodels import product
from flaskr.firestorethings import WriterFirestore

bp = Blueprint('productspages', __name__, url_prefix='/productspages')

@bp.route('/add', methods=('GET', 'POST'))
def add():
    if request.method=='POST':
        ide=request.form['ide']
        productName=request.form['productName']
        error=None
        if not ide:
            error='ide required'
        elif not productName:
            error='product Name required'
        else:
            try:
                productdata=product(ide,productName)
            except WrongDataException:
                error='Wrong data'
            else:
                productregister=WriterFirestore()
                try:
                    productregister.register(productdata.kind(),productdata.data())
                except RedundancyException:
                    error='trying to register an already registered product'
        if not(error is None):
            flash(error)
    return render_template('productspages/add.html')

