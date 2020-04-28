from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired

class CommandForm(FlaskForm):
    # Default way with parameter selection. Activate command option only in
    # differentc case
    command = StringField(label='Type your command here:', validators=[
        validators.optional(), validators.length(max=200)])

    ip1 = StringField('Sender IP address:', [validators.optional(),
        validators.length(max=15)])

    ip2 = StringField('Receiver IP address:', [validators.optional(),
        validators.length(max=15)])

    pkt_size = SelectField('Packet size distrbution (Don)', [DataRequired()],
        choices=[('-W', 'Weibull'), ('-U', 'Uniform'), ('-N', 'Normal'),
        ('-O', 'Poisson')])

    interval = SelectField('Inter departure interval distrbution (Doff)',
        [DataRequired()], choices=[('-w', 'Weibull'), ('-U', 'Uniform'),
        ('-n', 'Normal'), ('-p', 'Pareto')])

    protocol = SelectField('Protocol', [DataRequired()],
        choices=[('UDP', 'UDP'),('TCP', 'TCP')])

    duration = IntegerField('Flow duration (milliseconds)', [
        validators.optional()], default=1000)

    delay = IntegerField('Delay (milliseconds)', [validators.optional()],
        default=0)

    submit =  SubmitField('Submit')
