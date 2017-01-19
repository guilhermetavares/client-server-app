import os
import unittest

from app import app, db, create_machine_from_xml
from client import ServerClient

TEST_DB = 'test.db'
 
 
class ServerTestCase(unittest.TestCase):
 
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def get_xml_data(self):
        file_xml = open('config.xml')
        xml = file_xml.read()
        file_xml.close()
        return xml

    def get_encrypt_xml_data(self):
        file_xml = open('encrypt_xml_response.txt')
        xml = file_xml.read()
        file_xml.close()
        return xml

    def test_01_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_02_add_machine(self):
        response = self.app.get('/add/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/add/', data={'erorr': '1'}, follow_redirects=True)

        xml = self.get_xml_data()

        response = self.app.post('/add/', data={'xml': xml}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_03_client(self):
        machine = create_machine_from_xml(self.get_xml_data())
        server_client = ServerClient(machine)
        xml = self.get_encrypt_xml_data()

        data = server_client.decripty_xml(xml)
        self.assertTrue('cpu' in data)

        machine_data = server_client.create_data_from_xml(xml)
        self.assertTrue('MEMORY' in str(machine_data))


if __name__ == "__main__":
    unittest.main()
