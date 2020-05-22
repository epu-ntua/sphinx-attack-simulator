from app import app
from flask import render_template, request, redirect, flash
import flask
from app.forms import CommandForm
from app.utils import *
import os


@app.route('/')
@app.route('/home')
def entry_page():
    return render_template('entry_page.html')


@app.route('/vm_overview/', defaults={"nodeId": 0})
@app.route('/vm_overview/<int:nodeId>/', methods=['GET', 'POST'])
def vm_overview(nodeId):
    if request.method == 'POST':
        if "new_node_form" in request.form:
            name = request.form.get("node_name")
            add_new_node(name)
            return redirect("/vm_overview/0/")

        if "new_node_flow_form" in request.form:
            add_flow_to_node( request.form.get("flowToAdd"), nodeId, request.form.get("nodeTo"))
            return redirect("/vm_overview/0/")

        if "run_all" in request.form:
            run_flows()
            return redirect("/vm_overview/0/")

        if nodeId > 0:
            toRedirect = ""
            return redirect(toRedirect)
        else:
            return redirect("/vm_overview/0/")
    else:
        all_nodes = get_all_nodes()
        # for nodeIt in all_nodes:
        #     print(nodeIt.id)
        all_flows = get_all_flows()
        all_flow_to_node = get_all_flow_to_node()
    return render_template("vm_overview.html", nodeId=int(nodeId), all_nodes=all_nodes, all_flows = all_flows, all_flow_to_node = all_flow_to_node)


@app.route('/flow_creation/', defaults={"flowId": 0})
@app.route('/flow_creation/<int:flowId>/', methods=['GET', 'POST'])
def flow_creation(flowId):
    if request.method == 'POST':
        if "new_flow_form" in request.form:
            name = request.form.get("name")
            protocol = request.form.get("protocol")
            duration = request.form.get("duration")
            delay = request.form.get("delay")

            packet_size_distributions = request.form.get("packet_size_distributions")
            packet_size_distributions_value_1 = request.form.get("packet_size_distributions_value_1")
            packet_size_distributions_value_2 = request.form.get("packet_size_distributions_value_2")

            # packet_size_pkt_size = request.form.get("packet_size_pkt_size")
            # packet_size_min_pkt_size = request.form.get("packet_size_min_pkt_size")
            # packet_size_max_pkt_size = request.form.get("packet_size_max_pkt_size")
            # packet_size_average_pkt_size = request.form.get("packet_size_average_pkt_size")
            # packet_size_mean = request.form.get("packet_size_mean")
            # packet_size_std_dev = request.form.get("packet_size_std_dev")
            # packet_size_shape = request.form.get("packet_size_shape")
            # packet_size_scale = request.form.get("packet_size_scale")

            interdeparture_interval_distribution = request.form.get("interdeparture_interval_distribution")
            interdeparture_interval_distribution_1 = request.form.get("interdeparture_interval_distribution_1")
            interdeparture_interval_distribution_2 = request.form.get("interdeparture_interval_distribution_2")
            # interdeparture_rate = request.form.get("interdeparture_rate")
            # interdeparture_min_rate = request.form.get("interdeparture_min_rate")
            # interdeparture_max_rate = request.form.get("interdeparture_max_rate")
            # interdeparture_mean = request.form.get("interdeparture_mean")
            # interdeparture_std_dev = request.form.get("interdeparture_std_dev")
            # interdeparture_shape = request.form.get("interdeparture_shape")
            # interdeparture_scale = request.form.get("interdeparture_scale")

            add_new_flow(name, protocol, duration, delay, packet_size_distributions, packet_size_distributions_value_1,
                         packet_size_distributions_value_2,
                         interdeparture_interval_distribution,
                         interdeparture_interval_distribution_1, interdeparture_interval_distribution_2)

            return redirect("/flow_creation/0")
        if flowId != 0:
                print(request.form)

                toRedirect = ""
                return redirect(toRedirect)
        else:
                return redirect("/flow_creation/0/")
    else:
        all_flows = get_all_flows()
        return render_template('flow_creation.html', flowId=int(flowId), all_flows=all_flows)

@app.route('/enter-command', methods=['GET', 'POST'], defaults={"n_vm": 2})
def command(n_vm):
    form = CommandForm()
    if form.validate_on_submit():
        flash('Sent command to daemon machine: {}'.format(form.command.data))
        os.system(('../D-ITG/bin/' + str(form.command.data)))
        return redirect('/home')
    return render_template('enter-command.html', title='Commander', form=form,
                           n_vm=n_vm)
