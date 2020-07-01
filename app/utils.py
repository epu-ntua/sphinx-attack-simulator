from app.models import *
from app import db
from flask import flash
import os
import time


# Check if name exists and exclude names that already exist - standard name and syntax checks
# Grammar check in nodes
def add_new_node(name):
    new_node = Nodes(name=name)
    db.session.add(new_node)
    db.session.commit()


# def delete_node():
#
# def edit_node():

def get_all_nodes():
    return Nodes.query.all()


def get_all_flows():
    return Flows.query.all()


def get_all_on_off_flows():
    return FlowsOnOff.query.all()


# def delete_flow():
#
# def edit_flow():

def add_new_flow(name, protocol, duration, delay, packet_size_distributions, packet_size_distributions_value_1,
                 packet_size_distributions_value_2,
                 interdeparture_interval_distribution, interdeparture_interval_distribution_1,
                 interdeparture_interval_distribution_2):
    if packet_size_distributions_value_2 == "":
        packet_size_distributions_value_2 = 0

    if interdeparture_interval_distribution_2 == "":
        interdeparture_interval_distribution_2 = 0

    new_flow = Flows(name=name, protocol=protocol, duration=duration, delay=delay,
                     packet_size_distributions=packet_size_distributions,
                     packet_size_distributions_value_1=float(packet_size_distributions_value_1),
                     packet_size_distributions_value_2=float(packet_size_distributions_value_2),
                     interdeparture_interval_distribution=interdeparture_interval_distribution,
                     interdeparture_interval_distribution_value_1=float(interdeparture_interval_distribution_1),
                     interdeparture_interval_distribution_value_2=float(interdeparture_interval_distribution_2)
                     )

    db.session.add(new_flow)
    db.session.commit()


def add_new_on_off_flow(name, protocol, delay, ip_version, number_of_flow, don_minimum_permitted, don_maximum_permitted,
                        doff_minimum_permitted, doff_maximum_permitted,
                        don_distributions, don_distributions_value_1,
                        don_distributions_value_2,
                        doff_distributions, doff_distributions_value_1,
                        doff_distributions_value_2):
    if don_distributions_value_2 == "":
        don_distributions_value_2 = 0

    if doff_distributions_value_2 == "":
        doff_distributions_value_2 = 0

    new_flow = FlowsOnOff(name=name, protocol=protocol, delay=delay, ip_version=ip_version,
                          don_minimum_permitted=don_minimum_permitted,
                          don_maximum_permitted=don_maximum_permitted,
                          doff_minimum_permitted=doff_minimum_permitted,
                          doff_maximum_permitted=doff_maximum_permitted,
                          number_of_flow=number_of_flow,
                          don_distributions=don_distributions,
                          don_distributions_value_1=float(don_distributions_value_1),
                          don_distributions_value_2=float(don_distributions_value_2),
                          doff_distributions=doff_distributions,
                          doff_distributions_value_1=float(doff_distributions_value_1),
                          doff_distributions_value_2=float(doff_distributions_value_2)
                          )

    db.session.add(new_flow)
    db.session.commit()


def get_all_flow_to_node():
    return FlowToNode.query.all()


def get_flow_to_node(nodeId):
    return FlowToNode.query.filter(FlowToNode.fk_node_from == nodeId).all()


def get_flow_to_on_off_node(nodeId):
    return FlowOnOffToNode.query.filter(FlowOnOffToNode.fk_node_from == nodeId).all()


def add_flow_to_node(flowId, nodeFromId, nodeToId):
    new_connection = FlowToNode(fk_flow=flowId, fk_node_from=nodeFromId, fk_node_to=nodeToId)
    db.session.add(new_connection)
    db.session.commit()


def add_flow_to_node(flowId, nodeFromId, nodeToId):
    new_connection = FlowToNode(fk_flow=flowId, fk_node_from=nodeFromId, fk_node_to=nodeToId)
    db.session.add(new_connection)
    db.session.commit()


def add_flow_on_off_to_node(flowId, nodeFromId, nodeToId):
    new_connection = FlowOnOffToNode(fk_flow=flowId, fk_node_from=nodeFromId, fk_node_to=nodeToId)
    db.session.add(new_connection)
    db.session.commit()


def remove_flow_from_node(flowToNodeId):
    db.session.delete(flowToNodeId)
    db.session.commit()


def create_command(flow, node_from, node_to):
    # delay = flow.delay if flow.delay else 0
    command = "ITGManager " + str(node_from.name) + " -a " + str(node_to.name) + " -d " + str(
        flow.delay) + " -t " + str(int(flow.duration)) + " -T " + str(flow.protocol.value)

    if flow.interdeparture_interval_distribution.value == "constant":
        command = command + " -C " + str(flow.packet_size_distributions_value_1)
    elif flow.interdeparture_interval_distribution.value == "uniform":
        command = command + " -U " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)
    elif flow.interdeparture_interval_distribution.value == "exponential":
        command = command + " -E " + str(flow.packet_size_distributions_value_1)
    elif flow.interdeparture_interval_distribution.value == "normal":
        command = command + " -N " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)
    elif flow.interdeparture_interval_distribution.value == "poisson":
        command = command + " -O " + str(flow.packet_size_distributions_value_1)
    elif flow.interdeparture_interval_distribution.value == "pareto":
        command = command + " -V " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)
    elif flow.interdeparture_interval_distribution.value == "cauchy":
        command = command + " -Y " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)
    elif flow.interdeparture_interval_distribution.value == "gamma":
        command = command + " -G " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)
    elif flow.interdeparture_interval_distribution.value == "weibull":
        command = command + " -W " + str(flow.packet_size_distributions_value_1) + " " + str(
            flow.packet_size_distributions_value_2)

    if flow.packet_size_distributions.value == "constant":
        command = command + " -c " + str(flow.interdeparture_interval_distribution_value_1)
    elif flow.packet_size_distributions.value == "uniform":
        command = command + " -u " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)
    elif flow.packet_size_distributions.value == "exponential":
        command = command + " -e " + str(flow.interdeparture_interval_distribution_value_1)
    elif flow.packet_size_distributions.value == "normal":
        command = command + " -n " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)
    elif flow.packet_size_distributions.value == "poisson":
        command = command + " -o " + str(flow.interdeparture_interval_distribution_value_1)
    elif flow.packet_size_distributions.value == "pareto":
        command = command + " -v " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)
    elif flow.packet_size_distributions.value == "cauchy":
        command = command + " -y " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)
    elif flow.packet_size_distributions.value == "gamma":
        command = command + " -g " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)
    elif flow.packet_size_distributions.value == "weibull":
        command = command + " -w " + str(flow.interdeparture_interval_distribution_value_1) + " " + str(
            flow.interdeparture_interval_distribution_value_2)

    return command


def create_on_off_command(group_flow, node_from, node_to):
    # delay = group_flow.delay if group_flow.delay else 0
    command = "docker exec " + str(node_from.name) + " ./sourceonoff/sourceonoff --verbose "

    if group_flow.protocol == "tcp":
        command = command + "-t "
    elif group_flow.protocol == "udp":
        command = command + "-T "

    command = command + "--destination=" + str(node_to.name) + " "

    if group_flow.ip_version == "ipv4":
        command = command + "-4 "
    elif group_flow.ip_version == "ipv6":
        command = command + "-6 "

    command = command + "--don-type="

    if group_flow.don_distributions.value == "uniform":
        command = command + "Uniform"
    elif group_flow.don_distributions.value == "exponential":
        command = command + "Exponential --don-lambda=" + str(group_flow.don_distributions_value_1) + " "
    elif group_flow.don_distributions.value == "weibull":
        command = command + "Weibull --don-k=" + str(group_flow.don_distributions_value_1) + " --don-lambda=" + str(group_flow.don_distributions_value_2) + " "
    elif group_flow.don_distributions.value == "pareto":
        command = command + "Pareto --don-alpha=" + str(group_flow.don_distributions_value_1) + " --don-xm=" + str(group_flow.don_distributions_value_2) + " "
    elif group_flow.don_distributions.value == "poisson":
        command = command + "Poisson --don-lambda=" + str(group_flow.don_distributions_value_1) + " "
    else:
        print(group_flow.don_distributions)

    command = command + "--don-min=" + str(group_flow.don_minimum_permitted) + " --don-max=" + str(
        group_flow.don_maximum_permitted) + " "

    command = command + "--doff-type="

    if group_flow.doff_distributions.value == "uniform":
        command = command + "Uniform"
    elif group_flow.doff_distributions.value == "exponential":
        command = command + "Exponential --doff-lambda=" + str(group_flow.doff_distributions_value_1) + " "
    elif group_flow.doff_distributions.value == "weibull":
        command = command + "Weibull --doff-k=" + str(group_flow.doff_distributions_value_1) + " --doff-lambda=" + str(group_flow.doff_distributions_value_2) + " "
    elif group_flow.doff_distributions.value == "pareto":
        command = command + "Pareto --doff-alpha=" + str(group_flow.doff_distributions_value_1) + " --doff-xm=" + str(group_flow.doff_distributions_value_2) + " "
    elif group_flow.doff_distributions.value == "poisson":
        command = command + "Poisson --doff-lambda=" + str(group_flow.doff_distributions_value_1) + " "
    else:
        print(group_flow.doff_distributions)

    command = command + "--don-min=" + str(group_flow.doff_minimum_permitted) + " --don-max=" + str(
        group_flow.doff_maximum_permitted) + " "

    command = command + "--turns=" + str(group_flow.number_of_flow)
    return command


# We pass an array with Ids of nodes we want to run
def run_flows():
    all_nodes = Nodes.query.all()

    for node_from in all_nodes:
        # node_from = Nodes.query.filter(Nodes.id == node_to_run.id)
        flows_connections = FlowToNode.query.filter(FlowToNode.fk_node_from == node_from.id).all()

        if len(flows_connections) > 0:
            for flow_con in flows_connections:
                node_to = Nodes.query.filter(Nodes.id == flow_con.fk_node_to).all()
                flow = Flows.query.filter(Flows.id == flow_con.id).first()
                command = create_command(flow, node_from, node_to[0])
                # I implement delay with python cause it won't work
                # delay_in_sec = flow.delay / 1000
                # time.sleep(delay_in_sec)
                print(command)
                flash('Sent command to daemon machine: {}'.format(command))
                os.system(('../D-ITG/bin/' + str(command)))


def run_flows_on_off():
    all_nodes = Nodes.query.all()

    for node_from in all_nodes:
        # node_from = Nodes.query.filter(Nodes.id == node_to_run.id)
        flows_connections = FlowOnOffToNode.query.filter(FlowOnOffToNode.fk_node_from == node_from.id).all()

        if len(flows_connections) > 0:
            for flow_con in flows_connections:
                node_to = Nodes.query.filter(Nodes.id == flow_con.fk_node_to).all()
                group_flow = FlowsOnOff.query.filter(FlowsOnOff.id == flow_con.id).first()
                command = create_on_off_command(group_flow, node_from, node_to[0])

                print(command)
                flash('Sent command to daemon machine: {}'.format(command))
                # os.system(command)


def tcp_flood_attack(receiver, port):
    command = "docker exec sender  hping3 -c 15000 -d 120 -S -w 64 -p " + port + " --flood --rand-source " + receiver
    flash('Activating TCP flood attack: {}'.format(command))
    os.system(command)

# def create_command_on_off():

# def run_on_off_command():
