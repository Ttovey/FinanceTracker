from datetime import datetime
from flask import render_template, Blueprint, Markup, Response, send_file, request, jsonify, make_response
import random
from financeTracker.assets.routes import new_asset
from financeTracker.models import Asset, Networth, Debt, Spending
from sqlalchemy import desc, asc
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from financeTracker import db


main = Blueprint('main', __name__)


@main.route('/')
def index():
    assets = Asset.query.order_by(desc(Asset.value)).all()
    debts = Debt.query.all()
    asset_total = 0
    debts_total = 0
    for asset in assets:
        asset_total += asset.value
    for debt in debts:
        debts_total += debt.amount
    networth = round(asset_total - debts_total, 2)

    newNetworth = Networth(total=networth)
    newDate = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'

    prevNetworth = Networth.query.order_by(desc(Networth.date)).all()[0]
    prevDate = f'{prevNetworth.date.year}-{prevNetworth.date.month}-{prevNetworth.date.day}'
    if newDate == prevDate:
        print('Networth already exits, updating networth value.')
        prevNetworth.total = newNetworth.total
        print(newNetworth.total)
        print(prevNetworth.total)
        db.session.commit()
    else:
        print('Adding New Networth.')
        db.session.add(newNetworth)
        db.session.commit()

    if len(assets) >= 5:
        assets = assets[:5]

    spending = spendCatPrices()

    return render_template('main/chart.html', assets=assets, networth=networth, spending=spending)


@main.route('/pie_plot.png')
def plot_png():
    labels, data = get_assets()
    img = pie_chart(data, labels)
    return send_file(img, mimetype='img/png')


@main.route('/spending_plot.png')
def spend_png():
    labels, data = get_spending()
    img = pie_chart(data, labels)
    return send_file(img, mimetype='img/png')


@main.route('/line_plot.png')
def line_plot_png():
    dates, data = get_networth()
    img = line_plot(data, dates)
    return send_file(img, mimetype='img/png')


def line_plot(data, labels):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax = sns.set(style='darkgrid')
    sns.lineplot(x=labels, y=data)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return img


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


def get_networth():
    networth = Networth.query.order_by(asc(Networth.date)).all()
    dates = []
    net = []
    for nets in networth:
        date = f'{nets.date.year}-{nets.date.month}-{nets.date.day}'
        dates.append(date)
        net.append(nets.total)
    return dates, net


def get_spending():
    spending = Spending.query.all()[:8]
    categories = {}
    values = []
    names = []
    for spend in spending:
        categories[spend.type] = categories.get(spend.type, 0) + spend.amount

    for name in categories:
        names.append(name)
        values.append(round(categories[name], 2))

    return names, values


def spendCatPrices():
    spending = Spending.query.all()
    categories = {}
    ordered = []

    for spend in spending:
        categories[spend.type] = categories.get(spend.type, 0) + spend.amount

    for spend in categories:
        categories[spend] = round(categories[spend], 2)
        ordered.append([spend, categories[spend]])

    ordered.sort(key=lambda x: x[1])
    print(ordered)

    return ordered
