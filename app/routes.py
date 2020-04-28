from app import app
from flask import render_template, request, redirect, flash
import flask
from app.forms import CommandForm
import os


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

@app.route('/enter-command', methods=['GET', 'POST'], defaults={"n_vm": 2})
def command(n_vm):
    form = CommandForm()
    if form.validate_on_submit():
        flash('Sent command to daemon machine: {}'.format(form.command.data))
        os.system(os.path.join('~/D-ITG-2.8.1-r1023/bin/', str(
            form.command.data)))
        return redirect('/home')
    return render_template('enter-command.html', title='Commander', form=form,
        n_vm=n_vm)
