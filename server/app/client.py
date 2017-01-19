import sys
import re

from app import db, MachineCPUData

from subprocess import PIPE, Popen

# from paramiko import client
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent.parent))

from utils.encrypt import decrypt


class ServerClient(object):
    key = '32longbytesforemp786cuskey123cpt'

    def __init__(self, machine):
        self.machine = machine

    # def __init__(self, address, username, password):
 #          self.client = client.SSHClient()
 #          self.client.set_missing_host_key_policy(client.AutoAddPolicy())
 #          self.client.connect(
 #              address, username=username, password=password, look_for_keys=False)

    def create_data_from_xml(self, xml):
        machine_data = MachineCPUData(
            **self.get_machine_data_params(xml)
        )
        db.session.add(machine_data)
        db.session.commit()
        return machine_data

    def get_machine_data_params(self, xml):
        data = self.decripty_xml(xml)
        return {
            'machine_id': self.machine.id,
            'cpu_percent': float(data.get('cpu', {}).get('percent', 0)),
            'memory_total': float(data.get('memory', {}).get('total', 0)),
            'memory_percent': float(data.get('memory', {}).get('percent', 0)),
            'uptime': float(data.get('uptime', {}).get('time', 0)),
        }

    def get_xml_data(self, xml, key):
        try:
            e = re.compile('<{0}.*?>(.*?)</{0}>'.format(key))
            return e.findall(xml)[0]
        except:
            return None

    def decripty_xml(self, xml):
        decrypt_xml = decrypt(xml, key=self.key).decode()
        data = {}
        memory = self.get_xml_data(decrypt_xml, 'memory')
        if memory:
            data.update({
                'memory': {
                    'available': self.get_xml_data(memory, 'available'),
                    'used': self.get_xml_data(memory, 'used'),
                    'total': self.get_xml_data(memory, 'total'),
                    'free': self.get_xml_data(memory, 'free'),
                    'percent': self.get_xml_data(memory, 'percent'),
            }})
        uptime = self.get_xml_data(decrypt_xml, 'uptime')
        if uptime:
            data.update({
                'uptime': {
                    'actual': self.get_xml_data(uptime, 'actual'),
                    'formatted': self.get_xml_data(uptime, 'formatted'),
                    'boot': self.get_xml_data(uptime, 'boot'),
                    'time': self.get_xml_data(uptime, 'time'),
            }})
        cpu = self.get_xml_data(decrypt_xml, 'cpu')
        if cpu:
            data.update({
                'cpu': {
                    'percent': self.get_xml_data(memory, 'percent'),
            }})
        return data
