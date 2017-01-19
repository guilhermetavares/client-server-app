import unittest

from main import CPUData

KEY123 = '32longbytesforemp786cuskey123cpt'


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.cpu_data = CPUData()

    def test_01_get_memory(self):
        self.assertTrue('available' in self.cpu_data.get_memory())

    def test_02_get_cpu(self):
        self.assertTrue('percent' in self.cpu_data.get_cpu())

    def test_03_get_uptime(self):
        self.assertTrue('formatted' in self.cpu_data.get_uptime())

    def test_04_get_all_data(self):
        self.assertTrue('cpu' in self.cpu_data.get_all_data())

    def test_05_get_xml(self):
        self.assertTrue('xml' in str(self.cpu_data.get_xml()))

    def test_06_get_formatted_xml(self):
        self.assertTrue('<xml' in self.cpu_data.get_formatted_xml())

    def test_07_get_encrypt_xml(self):
        self.assertFalse(self.cpu_data.get_encrypt_xml(KEY123) is None)

    def test_08_run(self):
        import run
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
