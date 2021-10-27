from flask import render_template, Blueprint

assets = Blueprint('assets', __name__)


@assets.route('/assets')
def asset():
    return render_template('assets.html')
