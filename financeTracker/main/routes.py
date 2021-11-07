from flask import render_template, Blueprint, Markup, Response, send_file
import random
from financeTracker.models import Asset
from sqlalchemy import desc
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns


main = Blueprint('main', __name__)


@main.route('/')
def index():
    assets = Asset.query.order_by(desc(Asset.value)).all()
    if len(assets) >= 5:
        assets = assets[:5]
    return render_template('main/chart.html', assets=assets)


@main.route('/plot.png')
def plot_png():
    labels, data = get_assets()
    img = pie_chart(data, labels)
    return send_file(img, mimetype='img/png')


def pie_chart(data, labels):
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = sns.dark_palette((260, 75, 60), input="husl")[:5]
    plt.pie(data, labels=labels, colors=colors,
            autopct='%.0f%%', pctdistance=1.1, labeldistance=1.2)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return img


def get_assets():
    assets = Asset.query.all()
    values = []
    names = []
    for asset in assets:
        names.append(asset.name)
        values.append(asset.value)
    return names, values
