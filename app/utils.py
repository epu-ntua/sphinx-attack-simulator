from app.models import *
from app import db
from flask import flash
import os
import time


def add_new_node(name):
    new_node = Nodes(name=name)
    db.session.add(new_node)
    db.session.commit()


def get_all_nodes():
    return Nodes.query.all()


def get_all_flows():
    return Flows.query.all()


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


def get_all_flow_to_node():
    return FlowToNode.query.all()

def get_flow_to_node(nodeId):
    return FlowToNode.query.filter(FlowToNode.fk_node_from == nodeId).all()

def add_flow_to_node(flowId, nodeFromId, nodeToId):
    new_connection = FlowToNode(fk_flow=flowId, fk_node_from=nodeFromId, fk_node_to=nodeToId)
    db.session.add(new_connection)
    db.session.commit()

def remove_flow_from_node(flowToNodeId):
    db.session.delete(flowToNodeId)
    db.session.commit()


def create_command(flow, node_from, node_to):
    delay = flow.delay if flow.delay else 0
    command = "ITGManager " + str(node_from.name) + " -a " + str(node_to.name)+ " -t " + str(int(flow.duration)) + " -T " + str(flow.protocol.value)

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
                delay_in_sec = flow.delay / 1000
                time.sleep(delay_in_sec)
                print(command)
                flash('Sent command to daemon machine: {}'.format(command))
                os.system(('../D-ITG/bin/' + str(command)))
