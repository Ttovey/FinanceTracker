from flask import render_template, Blueprint, redirect, url_for, request
from financeTracker.models import Asset
from financeTracker.assets.forms import AssetForm, UpdateAssetForm
from financeTracker import db

assets = Blueprint('assets', __name__)


@assets.route('/assets')
def asset():
    Assets = Asset.query.all()
    total = 0
    for asset in Assets:
        total += asset.value
    total = round(total, 2)
    return render_template('assets/assets.html', Assets=Assets, total=total)


@assets.route('/assets/new', methods=['GET', 'POST'])
def new_asset():
    form = AssetForm()
    if form.validate_on_submit():
        newAsset = Asset(name=form.assetName.data, value=form.value.data)
        db.session.add(newAsset)
        db.session.commit()
        return redirect(url_for('assets.asset'))
    return render_template('assets/new_asset.html', form=form, title='New Asset')


@assets.route('/assets/<int:asset_id>/info', methods=['GET', 'POST'])
def asset_info(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return render_template('assets/asset_info.html', asset=asset)


@assets.route('/assets/<int:asset_id>/delete', methods=['POST'])
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return redirect(url_for('assets.asset'))


@assets.route('/assets/<int:asset_id>/update', methods=['GET', 'POST'])
def update_asset(asset_id):
    form = UpdateAssetForm()
    asset = Asset.query.get_or_404(asset_id)
    if form.validate_on_submit():
        asset.name = form.assetName.data
        asset.value = form.value.data
        db.session.commit()
        return redirect(url_for('assets.asset_info', asset_id=asset.id))
    elif request.method == 'GET':
        form.assetName.data = asset.name
        form.value.data = asset.value

    return render_template('assets/update_asset.html', asset=asset, form=form)
