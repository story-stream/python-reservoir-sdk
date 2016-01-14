from unittest import TestCase

from respy.utils import ArgumentConverter, ARGUMENT_CONVERTED_KEY


class ArgumentConverterTest(TestCase):

    def setUp(self):
        self.converter = ArgumentConverter()

    def test_add_converted_key_after_conversion(self):
        source_arguments = {
            'arg': 'test'
        }

        result = self.converter(**source_arguments)

        self.assertTrue(result[ARGUMENT_CONVERTED_KEY])

    def test_underscore_name_converts_to_dash(self):
        source_arguments = {
            'this_is_testing': 'test'
        }

        result = self.converter(**source_arguments)

        self.assertEqual(result, {
            'this-is-testing': 'test',
            ARGUMENT_CONVERTED_KEY: True
        })

    def test_doesnt_convert_boolean_to_lowercase(self):
        source_arguments = {
            'truthey': True,
            'falsey': False
        }

        result = self.converter(**source_arguments)

        self.assertEqual(result, {
            'truthey': True,
            'falsey': False,
            ARGUMENT_CONVERTED_KEY: True
        })

    def test_q_list_seperated_by_OR(self):
        query = ['test1=true', 'test2=false']
        source_arguments = {
            'q': query
        }

        result = self.converter(**source_arguments)

        self.assertEqual(result, {
            'q': ' OR '.join(query),
            ARGUMENT_CONVERTED_KEY: True
        })

    def test_ids_list_returned_as_ids_list(self):
        ids = [1, 2, 3, 4, 5]
        source_arguments = {
            'ids': ids
        }

        result = self.converter(**source_arguments)

        self.assertEqual(result, {
            'ids': [1,2,3,4,5],
            ARGUMENT_CONVERTED_KEY: True
        })
