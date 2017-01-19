import psutil
import time

import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from utils.xml_utils import dict2xml
from utils.encrypt import encrypt, decrypt


class CPUData(object):

    def __init__(self, key=None):
        pass

    def get_encrypt_xml(self, key):
        return encrypt(self.get_formatted_xml(), key)

    def get_formatted_xml(self):
        return self.get_xml().toxml()

    def get_xml(self):
        return dict2xml({'xml': self.get_all_data()})

    def get_all_data(self):
        return {
            'memory': self.get_memory(),
            'cpu': self.get_cpu(),
            'uptime': self.get_uptime(),
        }

    def get_uptime(self):
        actual_time = time.time()
        boot_time = psutil.boot_time()
        return {
            'actual': actual_time,
            'boot': boot_time,
            'time': actual_time - boot_time,
            'formatted': int(actual_time - boot_time),
        }
    
    def get_cpu(self):
        return {
            'percent': psutil.cpu_percent(interval=1),
        }

    def get_memory(self):
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent,
        }
