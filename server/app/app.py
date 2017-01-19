import os
import re

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

from datetime import datetime

app = Flask(__name__)
# app.config['SQLAlchemy_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/crossover'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{0}database.db".format(os.path.dirname(os.path.abspath(__file__)))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ['MAIL_USERNAME'],
    MAIL_PASSWORD=os.environ['MAIL_PASSWORD'],
)

mail = Mail(app)
db = SQLAlchemy(app)


class Machine(db.Model):
    __tablename__ = 'Machine'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    port = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)

    memory_limit = db.Column(db.Float)
    cpu_limit = db.Column(db.Float)

    cpu_data_set = db.relationship('MachineCPUData', backref='machine', lazy='dynamic')

    def __init__(self, ip_address, username, password, email, port, memory_limit, cpu_limit):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.email = email
        self.port = port
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.date_added = datetime.utcnow()

    def __repr__(self):
        return '<IP %r>' % self.ip_address

    def get_data(self):
        return MachineCPUData.query.filter_by(machine_id=self.id).first()


def create_machine_from_xml(xml_data):
    def get_xml_data(xml, key, format_str='{0}="(.*?)"'):
        try:
            return re.compile(format_str.format(key)).findall(xml)[0]
        except IndexError:
            return ''
    params = {
        'ip_address': get_xml_data(xml_data, 'ip'),
        'port': int(get_xml_data(xml_data, 'port') or 8000),
        'username': get_xml_data(xml_data, 'username'),
        'password': get_xml_data(xml_data, 'password'),
        'email': get_xml_data(xml_data, 'mail'),
        'memory_limit': float(get_xml_data(xml_data, 'memory', 'type="{0}" limit="(.*?)%"') or 0),
        'cpu_limit': float(get_xml_data(xml_data, 'cpu', 'type="{0}" limit="(.*?)%"') or 0),
    }
    machine = Machine(**params)
    db.session.add(machine)
    db.session.commit()
    return machine


class MachineCPUData(db.Model):
    __tablename__ = 'MachineCPUData'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('Machine.id'))
    cpu_percent = db.Column(db.Float)
    memory_total = db.Column(db.Float)
    memory_percent = db.Column(db.Float)
    uptime = db.Column(db.Float)

    def __init__(self, machine_id, cpu_percent, memory_total, memory_percent, uptime):
        self.machine_id = machine_id
        self.cpu_percent = cpu_percent
        self.memory_total = memory_total
        self.memory_percent = memory_percent
        self.uptime = uptime

    def __repr__(self):
        return 'CPU %r MEMORY %r / %r UPTIME %r' % (self.cpu_percent, self.memory_total, self.memory_percent, self.uptime)


@app.route('/add/', methods=['GET', 'POST'])
def add_machine():
    if request.method == 'POST':
        if 'xml' in request.form:
            create_machine_from_xml(request.form['xml'])
    return redirect(url_for('main'))


@app.route('/update/')
def add_numbers():
    from client import ServerClient

    machines = Machine.query.all()
    for machine in machines:
        client = ServerClient(machine)
        client.update()

    return jsonify(status=True)


@app.route("/")
def main():
    return render_template('index.html', machine_list=Machine.query.all())


if __name__ == "__main__":
    app.run()
