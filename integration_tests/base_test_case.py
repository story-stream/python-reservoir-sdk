import unittest
from respy import Reservoir

class ResponseParser(object):
    @staticmethod
    def extract_data(response, *keys):
        if not keys:
            return response['results']

        data = []
        for record in response['results']:
            obj = {}
            for k in keys:
                obj[k] = record[k]
            data.append(obj)
        return data


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Reservoir(base_url='http://localhost:3000')
        self.parser = ResponseParser
