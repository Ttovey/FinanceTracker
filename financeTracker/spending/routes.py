from flask import render_template, Blueprint

spending = Blueprint('spending', __name__)


@spending.route('/spending')
def spend():
    return render_template('spending.html')
