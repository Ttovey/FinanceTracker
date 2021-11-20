from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from financeTracker.models import Spending
from financeTracker.spending.forms import SpendForm, UpdateSpendForm
from financeTracker import db
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.api import plaid_api
import os
import plaid
import datetime

spending = Blueprint('spending', __name__)

access_token = os.environ.get('PLAID_ACCESS_TOKEN')

PLAID_CLIENT_ID = os.environ.get(
    'PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


@spending.route('/spending')
def spend():
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30))
    end_date = datetime.datetime.now()
    Spends = Spending.query.all()
    spendTotal = 0
    for spend in Spends:
        if not start_date <= spend.date <= end_date:
            Spends.pop(spend)
        spendTotal += spend.amount
    spendTotal = round(spendTotal, 2)
    return render_template('spending/spending.html', Spends=Spends, total=spendTotal, length=len(Spends))


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


@spending.route('/plaid/transactions', methods=['GET'])
def get_transactions():
    # Pull transactions for the last 30 days
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30))
    end_date = datetime.datetime.now()
    try:
        options = TransactionsGetRequestOptions()
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date(),
            options=options
        )
        response = client.transactions_get(request)
        for transaction in response.to_dict()['transactions']:
            name = (transaction['name'])
            amount = (transaction['amount'])
            transaction_id = (transaction['transaction_id'])
            type = ''
            category = transaction['category']
            print(category)
            if 'Shops' in category:
                type = 'Super'
                type = category[1]
            elif 'Food and Drink' in category:
                type = category[1]
            elif 'Community' in category:
                type = category[1]
            else:
                type = category[0]

            spend = Spending.query.filter_by(
                transaction_id=transaction_id).first()

            if not spend and '-' not in str(amount):
                newSpend = Spending(name=name, amount=amount, type=type,
                                    transaction_id=transaction_id)
                db.session.add(newSpend)
                db.session.commit()

        return redirect(url_for('spending.spend'))
    except plaid.ApiException as e:

        return render_template('spending/spending.html')

# temporary spend deletion route


@spending.route('/spending/delete/all', methods=['GET', 'POST'])
def delete_all():
    spends = Spending.query.all()
    for spend in spends:
        db.session.delete(spend)
        db.session.commit()
