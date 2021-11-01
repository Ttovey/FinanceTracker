from flask import render_template, Blueprint, Markup

main = Blueprint('main', __name__)


@main.route('/')
def index():
    labels = ["January", "February", "March",
              "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('main/chart.html', values=values, labels=labels)
