from app import db
from enum import Enum

class protocolEnum(Enum):
    tcp = "tcp"
    udp = "udp"

class InternetProtocolEnum(Enum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"


class packetSizeDistributionsEnum(Enum):
    constant = "constant"
    uniform = "uniform"
    exponential = "exponential"
    normal = "normal"
    poisson = "poisson"
    pareto = "pareto"
    cauchy = "cauchy"
    gamma = "gamma"
    weibull = "weibull"

class interdepartureIntervalDistributionEnum(Enum):
    constant = "constant"
    uniform = "uniform"
    exponential = "exponential"
    normal = "normal"
    poisson = "poisson"
    pareto = "pareto"
    cauchy = "cauchy"
    gamma = "gamma"
    weibull = "weibull"

class OnOffEnum(Enum):
    uniform = "uniform"
    exponential = "exponential"
    poisson = "poisson"
    pareto = "pareto"
    weibull = "weibull"

class FlowToNode(db.Model):
    __tablename__ = 'FlowToNode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_flow = db.Column(db.Integer, db.ForeignKey('flows.id'))
    fk_node_from = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    fk_node_to = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    # Need to apply active functionality
    active = db.Column(db.Binary)

    def __repr__(self):
        return '<Flow {} , From {} ,To {}>'.format(self.fk_flow , self.fk_node_from , self.fk_node_to)

class FlowOnOffToNode(db.Model):
    __tablename__ = 'FlowOnOffToNode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_flow = db.Column(db.Integer, db.ForeignKey('flows_on_off.id'))
    fk_node_from = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    fk_node_to = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    # Need to apply active functionality
    active = db.Column(db.Binary)

    def __repr__(self):
        return '<Flow {} , From {} ,To {}>'.format(self.fk_flow , self.fk_node_from , self.fk_node_to)


class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())

    # Need to apply active functionality
    active = db.Column(db.Binary)

    node_to = db.relationship('FlowToNode' , backref = "to", primaryjoin=id==FlowToNode.fk_node_to)
    node_from = db.relationship('FlowToNode' , backref = "from", primaryjoin=id==FlowToNode.fk_node_from)

    node_to_on_off = db.relationship('FlowOnOffToNode', backref="to_on_off", primaryjoin=id == FlowOnOffToNode.fk_node_to)
    node_from_on_off = db.relationship('FlowOnOffToNode', backref="from_on_off", primaryjoin=id == FlowOnOffToNode.fk_node_from)
    def __repr__(self):
        return '<Node {}>'.format(self.name)

class Flows(db.Model):
    __tablename__ = 'flows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node = db.relationship('FlowToNode', backref = 'flow', primaryjoin=id==FlowToNode.fk_flow)
    name = db.Column(db.String)
    protocol = db.Column(db.Enum(protocolEnum))
    duration = db.Column(db.Integer)  # Duration in ms
    delay = db.Column(db.Integer)  # Delay in ms

    packet_size_distributions = db.Column(db.Enum(packetSizeDistributionsEnum))

    packet_size_distributions_value_1 =  db.Column(db.Float)
    packet_size_distributions_value_2 =  db.Column(db.Float)


    interdeparture_interval_distribution = db.Column(db.Enum(interdepartureIntervalDistributionEnum))

    interdeparture_interval_distribution_value_1 = db.Column(db.Float)
    interdeparture_interval_distribution_value_2 = db.Column(db.Float)


    def __repr__(self):
        return 'Flow {}'.format(self.name)



class FlowsOnOff(db.Model):
    __tablename__ = 'flows_on_off'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    node_target = db.relationship('FlowOnOffToNode', backref = 'flow', primaryjoin=id==FlowOnOffToNode.fk_flow)
    # node_source = db.relationship('FlowToNode', backref = 'flow', primaryjoin=id==FlowToNode.fk_flow)

    name = db.Column(db.String)

    protocol = db.Column(db.Enum(protocolEnum))
    delay = db.Column(db.Integer)  # Delay in nanosec
    ip_version = db.Column(db.Enum(InternetProtocolEnum))

    # Number of flow less that 999999. If equals 1000000 then it is infinite
    number_of_flow =db.Column(db.Integer)

    # All units in the distributions are nanoseconds
    don_distributions = db.Column(db.Enum(OnOffEnum))

    don_distributions_value_1 = db.Column(db.Float)
    don_distributions_value_2 = db.Column(db.Float)

    don_minimum_permitted = db.Column(db.Integer)
    don_maximum_permitted = db.Column(db.Integer)

    doff_distributions = db.Column(db.Enum(OnOffEnum))

    doff_distributions_value_1 =  db.Column(db.Float)
    doff_distributions_value_2 =  db.Column(db.Float)

    doff_minimum_permitted = db.Column(db.Integer)
    doff_maximum_permitted = db.Column(db.Integer)

    def __repr__(self):
        return 'Flow {}'.format(self.name)

#class
# 
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
