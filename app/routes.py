from app import app
from flask import render_template, request, redirect
import flask


@app.route('/')
@app.route('/home')
def entry_page():
    return render_template('entry_page.html')


@app.route('/vm_overview/', defaults={"asset": -1})
@app.route('/vm_overview/<int:asset>/', methods=['GET', 'POST'])
def vm_overview(asset):
    assetsArray = [1, 2, 3]
    proposedCVEArray = [1, 2, 3]
    othersCVEArray = [4, 5]

    return render_template('vm_overview.html', asset=asset, assetsArray=assetsArray, proposedCVEArray=proposedCVEArray,
                               othersCVEArray=othersCVEArray)
