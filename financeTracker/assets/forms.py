from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired


class AssetForm(FlaskForm):
    assetName = StringField('Asset Name', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Add Asset')


class UpdateAssetForm(FlaskForm):
    assetName = StringField('Asset Name', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Update Asset')
