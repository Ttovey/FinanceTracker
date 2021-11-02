from flask import Blueprint, redirect, url_for
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.api import plaid_api
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from financeTracker.models import Asset
from financeTracker import db
import plaid
import base64
import os
import datetime
import json
import time
from dotenv import load_dotenv
from werkzeug.wrappers import response
import os
from financeTracker.assets.forms import AssetForm


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

access_token = os.environ.get('PLAID_ACCESS_TOKEN')
item_id = os.environ.get('PLAID_ACCESS_TOKEN')
print(PLAID_CLIENT_ID)

plaidapi = Blueprint('plaid', __name__)


@plaidapi.route('/plaid/api')
def plaid():
    return 'connected'


@plaidapi.route('/plaid/accounts', methods=['GET', 'POST'])
def get_accounts():
    form = AssetForm()
    try:
        req = AccountsGetRequest(
            access_token=access_token
        )
        accounts_response = client.accounts_get(req)
    except plaid.ApiException as e:
        response = json.loads(e.body)
        return jsonify({'error': {'status_code': e.status, 'display_message':
                        response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}})

    data = accounts_response.to_dict()
    name = data['accounts'][0]['name']
    balance = data['accounts'][0]['balances']['available']

    if request.method == 'POST':
        if Asset.query.filter_by(name=name).all():
            asset = Asset.query.filter_by(name=name).first()
            asset.value = balance
            db.session.commit()
        else:
            asset = Asset(name=name, value=balance)
            db.session.add(asset)
            db.session.commit()
        return redirect(url_for('assets.asset'))

    form.assetName.data = name
    form.value.data = balance
    return render_template('assets/new_asset.html', form=form)


@plaidapi.route('/plaid/transactions', methods=['GET'])
def get_transactions():
    # Pull transactions for the last 30 days
    start_date = (datetime.datetime.now() - timedelta(days=30))
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
        print(response.to_dict())
        return response.to_dict()
    except plaid.ApiException as e:

        return jsonify(e)
