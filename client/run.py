import os
from main import CPUData
# xml = CPUData().get_encrypt_xml(key=os.getenv('CLIENT_ENCRIPT_KEY', '32longbytesforemp786cuskey123cpt'))
xml = CPUData().get_encrypt_xml(key='32longbytesforemp786cuskey123cpt')
print(xml)