from app import db
from enum import Enum

class protocolEnum(Enum):
    tcp = "tcp"
    udp = "udp"

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


class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())

    # Need to apply active functionality
    active = db.Column(db.Binary)

    node_to = db.relationship('FlowToNode' , backref = "to", primaryjoin=id==FlowToNode.fk_node_to)
    node_from = db.relationship('FlowToNode' , backref = "from", primaryjoin=id==FlowToNode.fk_node_from)
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

    # packet_size_pkt_size = db.Column(db.Float)
    # packet_size_min_pkt_size = db.Column(db.Float)
    # packet_size_max_pkt_size = db.Column(db.Float)
    # packet_size_average_pkt_size = db.Column(db.Float)
    # packet_size_mean = db.Column(db.Float)
    # packet_size_std_dev = db.Column(db.Float)
    # packet_size_shape = db.Column(db.Float)
    # packet_size_scale = db.Column(db.Float)

    interdeparture_interval_distribution = db.Column(db.Enum(interdepartureIntervalDistributionEnum))

    interdeparture_interval_distribution_value_1 = db.Column(db.Float)
    interdeparture_interval_distribution_value_2 = db.Column(db.Float)
    # interdeparture_rate = db.Column(db.Float)
    # interdeparture_min_rate = db.Column(db.Float)
    # interdeparture_max_rate = db.Column(db.Float)
    # interdeparture_mean = db.Column(db.Float)
    # interdeparture_std_dev = db.Column(db.Float)
    # interdeparture_shape = db.Column(db.Float)
    # interdeparture_scale = db.Column(db.Float)

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
