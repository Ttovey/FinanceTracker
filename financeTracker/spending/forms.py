from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired


class SpendForm(FlaskForm):
    spendName = StringField('Spend Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Spend')


class UpdateSpendForm(FlaskForm):
    spendName = StringField('Spend Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Update Spend')
