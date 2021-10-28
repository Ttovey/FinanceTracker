from flask import render_template, Blueprint, redirect, url_for, request
from financeTracker.models import Debt
from financeTracker.debts.forms import DebtForm, UpdateDebtForm
from financeTracker import db

debts = Blueprint('debts', __name__)


@debts.route('/debts')
def debt():
    Debts = Debt.query.all()
    totalDebt = 0
    for debt in Debts:
        totalDebt += debt.amount

    return render_template('debts/debts.html', Debts=Debts, total=totalDebt)


@debts.route('/debts/new', methods=['GET', 'POST'])
def new_debt():
    form = DebtForm()
    if form.validate_on_submit():
        newDebt = Debt(name=form.debtName.data, amount=form.amount.data)
        db.session.add(newDebt)
        db.session.commit()
        return redirect(url_for('debts.debt'))
    return render_template('/debts/new_debt.html', form=form)


@debts.route('/debts/<int:debt_id>/info', methods=['GET'])
def debt_info(debt_id):
    debt = Debt.query.get_or_404(debt_id)
    return render_template('debts/debt_info.html', debt=debt)


@debts.route('/debts/<int:debt_id>/update', methods=['GET', 'POST'])
def update_debt(debt_id):
    form = UpdateDebtForm()
    debt = Debt.query.get_or_404(debt_id)
    if form.validate_on_submit():
        debt.name = form.debtName.data
        debt.amount = form.amount.data
        db.session.commit()
        return redirect(url_for('debts.debt_info', debt_id=debt.id))
    elif request.method == 'GET':
        form.debtName.data = debt.name
        form.amount.data = debt.amount

    return render_template('debts/update_debt.html', debt=debt, form=form)


@debts.route('/debts/<int:debt_id>/delete', methods=['POST'])
def delete_debt(debt_id):
    debt = Debt.query.get_or_404(debt_id)
    db.session.delete(debt)
    db.session.commit()
    return redirect(url_for('debts.debt'))
