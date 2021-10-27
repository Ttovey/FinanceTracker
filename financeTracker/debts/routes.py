from flask import render_template, Blueprint

debts = Blueprint('debts', __name__)


@debts.route('/debts')
def debt():
    return render_template('debts.html')
