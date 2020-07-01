from app import app
from flask import render_template, request, redirect, flash
import flask
from app.forms import CommandForm
from app.utils import *
from app.globals import *
import os


@app.context_processor
def serverInfo():
    return dict(serverAddress=serverAddress, serverPort=serverPort)


@app.route('/')
@app.route('/home')
def entry_page():
    return render_template('entry_page.html')


@app.route('/tcp_flood/', methods=['GET', 'POST'])
def tcp_flood():
    if request.method == 'POST':
        if "run_attack" in request.form:
            tcp_flood_attack( request.form.get("node_target"),  request.form.get("target_port"))
            return redirect("/tcp_flood/")
    else:
        all_nodes = get_all_nodes()

        return render_template('tcp_flood.html', all_nodes = all_nodes)


@app.route('/vm_overview/', defaults={"nodeId": 0})
@app.route('/vm_overview/<int:nodeId>/', methods=['GET', 'POST'])
def vm_overview(nodeId):
    if request.method == 'POST':
        if "new_node_form" in request.form:
            name = request.form.get("node_name")
            add_new_node(name)
            return redirect("/vm_overview/0/")

        if "new_node_flow_form" in request.form:
            add_flow_to_node(request.form.get("flowToAdd"), nodeId, request.form.get("nodeTo"))
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
        all_flow_to_node = get_flow_to_node(nodeId)
    return render_template("vm_overview.html", nodeId=int(nodeId), all_nodes=all_nodes, all_flows=all_flows,
                           all_flow_to_node=all_flow_to_node)


@app.route('/vm_overview_on_off/', defaults={"nodeId": 0})
@app.route('/vm_overview_on_off/<int:nodeId>/', methods=['GET', 'POST'])
def vm_overview_on_off(nodeId):
    if request.method == 'POST':
        if "new_node_form" in request.form:
            name = request.form.get("node_name")
            add_new_node(name)
            return redirect("/vm_overview_on_off/0/")

        if "new_node_flow_form" in request.form:
            add_flow_on_off_to_node(request.form.get("flowToAdd"), nodeId, request.form.get("nodeTo"))
            return redirect("/vm_overview_on_off/0/")

        if "run_all" in request.form:
            run_flows_on_off()
            return redirect("/vm_overview_on_off/0/")

        if nodeId > 0:
            toRedirect = ""
            return redirect(toRedirect)
        else:
            return redirect("/vm_overview_on_off/0/")
    else:
        all_nodes = get_all_nodes()
        # for nodeIt in all_nodes:
        #     print(nodeIt.id)
        all_flow_on_off_node = get_flow_to_on_off_node(nodeId)
        for flowIt in all_flow_on_off_node:
            print(flowIt.id)
        all_flow_on_off = get_all_on_off_flows()
    return render_template("vm_overview_on_off.html", nodeId=int(nodeId), all_nodes=all_nodes,
                           all_flow_on_off=all_flow_on_off,
                           all_flow_on_off_node=all_flow_on_off_node)


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

            interdeparture_interval_distribution = request.form.get("interdeparture_interval_distribution")
            interdeparture_interval_distribution_1 = request.form.get("interdeparture_interval_distribution_1")
            interdeparture_interval_distribution_2 = request.form.get("interdeparture_interval_distribution_2")

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


@app.route('/on_off_flow_creation/', defaults={"groupFlowId": 0})
@app.route('/on_off_flow_creation/<int:groupFlowId>/', methods=['GET', 'POST'])
def on_off_flow_creation(groupFlowId):
    if request.method == 'POST':
        if "new_group_flow_form" in request.form:
            name = request.form.get("name")
            protocol = request.form.get("protocol")
            delay = request.form.get("delay")
            ip_version = request.form.get("ip_version")
            number_of_flow = request.form.get("number_of_flow")

            don_distributions = request.form.get("don_distributions")
            don_distributions_value_1 = request.form.get("don_distributions_value_1")
            don_distributions_value_2 = request.form.get("don_distributions_value_2")

            don_minimum_permitted = request.form.get("don_minimum_permitted")
            don_maximum_permitted = request.form.get("don_maximum_permitted")

            doff_distributions = request.form.get("doff_distributions")
            doff_distributions_value_1 = request.form.get("doff_distributions_value_1")
            doff_distributions_value_2 = request.form.get("doff_distributions_value_2")

            doff_minimum_permitted = request.form.get("doff_minimum_permitted")
            doff_maximum_permitted = request.form.get("doff_maximum_permitted")

            add_new_on_off_flow(name, protocol, delay, ip_version, number_of_flow,
                                don_minimum_permitted, don_maximum_permitted,
                                doff_minimum_permitted, doff_maximum_permitted,
                                don_distributions, don_distributions_value_1,
                                don_distributions_value_2,
                                doff_distributions, doff_distributions_value_1,
                                doff_distributions_value_2)

            return redirect("/on_off_flow_creation/0")
        if groupFlowId != 0:
            print(request.form)

            toRedirect = ""
            return redirect(toRedirect)
        else:
            return redirect("/on_off_flow_creation/0/")
    else:
        all_flows = get_all_on_off_flows()
        return render_template('on_off_creation.html', groupFlowId=int(groupFlowId), all_flows=all_flows)


@app.route('/enter-command', methods=['GET', 'POST'], defaults={"n_vm": 2})
def command(n_vm):
    form = CommandForm()
    if form.validate_on_submit():
        flash('Sent command to daemon machine: {}'.format(form.command.data))
        os.system(('../D-ITG/bin/' + str(form.command.data)))
        return redirect('/home')
    return render_template('enter-command.html', title='Commander', form=form,
                           n_vm=n_vm)
