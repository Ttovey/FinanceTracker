from flask import render_template, Blueprint, request, redirect, url_for
from financeTracker.models import Spending
from financeTracker.spending.forms import SpendForm, UpdateSpendForm
from financeTracker import db

spending = Blueprint('spending', __name__)


@spending.route('/spending')
def spend():
    Spends = Spending.query.all()
    spendTotal = 0
    for spend in Spends:
        spendTotal += spend.amount
    spendTotal = round(spendTotal, 2)
    return render_template('spending/spending.html', Spends=Spends, total=spendTotal)


@spending.route('/spending/new', methods=['GET', 'POST'])
def new_spend():
    form = SpendForm()
    if form.validate_on_submit():
        newSpend = Spending(name=form.spendName.data, amount=form.amount.data)
        db.session.add(newSpend)
        db.session.commit()
        return redirect(url_for('spending.spend'))
    return render_template('spending/new_spend.html', form=form)


@spending.route('/spending/<int:spend_id>/update', methods=['GET', 'POST'])
def update_spend(spend_id):
    form = UpdateSpendForm()
    spend = Spending.query.get_or_404(spend_id)
    if form.validate_on_submit():
        spend.name = form.spendName.data
        spend.amount = form.amount.data
        db.session.commit()
        return redirect(url_for('spending.spend_info', spend_id=spend.id))
    elif request.method == 'GET':
        form.spendName.data = spend.name
        form.amount.data = spend.amount
    return render_template('spending/update_spend.html', form=form, spend=spend)


@spending.route('/spending/<int:spend_id>/info')
def spend_info(spend_id):
    spend = Spending.query.get_or_404(spend_id)
    return render_template('spending/spend_info.html', spend=spend)


@spending.route('/spending/<int:spend_id>/delete', methods=['POST'])
def delete_spend(spend_id):
    spend = Spending.query.get_or_404(spend_id)
    db.session.delete(spend)
    db.session.commit()
    return redirect(url_for('spending.spend'))
