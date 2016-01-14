import re
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
        self.steps_to_undo = []

    def tearDown(self):
        if self.steps_to_undo:
            for step in self.steps_to_undo:
                endpoint = getattr(self.client, step['endpoint'])
                fnc = getattr(endpoint, step['inverse_method'])
                args = step['args']
                kwargs = step['kwargs']

                fnc(*args, **kwargs)

        self.steps_to_undo = []

    def reverse_on_tear_down(self, func, *args, **kwargs):
        calling_object = re.search(r'\.(?P<endpoint>[a-z]+)$', func.im_self.__module__).groupdict().get('endpoint')
        inverse_method = 'add' if func.__name__ == 'delete' else 'delete'

        self.steps_to_undo.append({
            'endpoint': calling_object,
            'inverse_method': inverse_method,
            'args': args,
            'kwargs': kwargs
        })

        return func(*args, **kwargs)
