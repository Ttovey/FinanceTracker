from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from polygon import RESTClient
import datetime

poly = Blueprint('poly', __name__)


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


@poly.route('/poly')
def polygon():
    key = 'fIImjjcMMqWkvysnEa361gqQ8peH5hRr'
    # RESTClient can be used as a context manager to facilitate closing the underlying http session
    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        from_ = "2021-01-01"
        to = "2021-02-01"
        resp = client.stocks_equities_aggregates(
            "AAPL", 1, "minute", from_, to, unadjusted=False)

        print(f"Minute aggregates for {resp.ticker} between {from_} and {to}.")

        for result in resp.results:
            dt = ts_to_datetime(result["t"])
            print(
                f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
        return redirect(url_for('assets.asset'))


@poly.route('/bitcoin')
def bitcoin():
    key = 'fIImjjcMMqWkvysnEa361gqQ8peH5hRr'

    with RESTClient(key) as client:
        from_ = 'BTC'
        to = 'USD'
        # Making lookup date to always be day before today
        date = datetime.date.today() - datetime.timedelta(1)
        resp = client.crypto_daily_open_close(
            from_, to, date, unadjusted=False
        )

    btc_price = resp.close

    return f'{btc_price}'
