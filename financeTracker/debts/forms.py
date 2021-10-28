from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.core import IntegerField, StringField


class DebtForm(FlaskForm):
    debtName = StringField('Debt Name', validators=[DataRequired()])
    amount = IntegerField('Debt Amount', validators=[DataRequired()])
    submit = SubmitField('Add Debt')


class UpdateDebtForm(FlaskForm):
    debtName = StringField('Debt Name', validators=[DataRequired()])
    amount = IntegerField('Debt Amount', validators=[DataRequired()])
    submit = SubmitField('Update Debt')
