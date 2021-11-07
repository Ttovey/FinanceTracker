from financeTracker import db
from datetime import datetime


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Asset({self.name}, {self.value})"


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Debt({self.name}, {self.amount})"


class Spending(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False, default='Other')
    transaction_id = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netWorth = db.Column(db.Integer, nullable=False)
