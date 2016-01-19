from base_test_case import BaseTestCase


class BaseIntegration(BaseTestCase):
    def __init__(self, methodName='runTest'):
        super(BaseIntegration, self).__init__(methodName)

        self.__default_data_feeds = [
            {'type': 'twitter', 'search': '#bluemonday'}
        ]

    def get_only_keys(self, story, *keys, **kwargs):
        response = self.get_full(story, **kwargs)
        return self.parser.extract_data(response, *keys)

    def get_full(self, story, **kwargs):
        endpoint = kwargs.pop('endpoint', None)
        if endpoint:
            endpoint = self._get_base_data_endpoint(endpoint)
        else:
            endpoint = self._get_endpoint_for_integration()
        return endpoint.all(story, self.__default_data_feeds, **kwargs)

    def traverse_newer_pages(self, story_id, limit=5, number_of_pages=10, newer_than=None):
        criteria = {
            'story': story_id,
            'feeds': self.__default_data_feeds,
            'limit': limit
        }

        if newer_than:
            criteria['newer_than'] = newer_than

        endpoint = self._get_endpoint_for_integration()

        calls = 0
        pages = []
        while calls < number_of_pages:
            calls += 1
            response = endpoint.all(**criteria)
            if not response.results:
                break

            pages.append(response.results)
            criteria['newer_than'] = response.meta.pagination.since.since

        return pages

    def traverse_older_pages(self, story_id, limit=5, number_of_pages=10, older_than=None):
        criteria = {
            'story': story_id,
            'feeds': self.__default_data_feeds,
            'limit': limit
        }

        if older_than:
            criteria['older_than'] = older_than

        endpoint = self._get_endpoint_for_integration()

        calls = 0
        pages = []
        while calls < number_of_pages:
            calls += 1
            response = endpoint.all(**criteria)
            if not response.results:
                break

            pages.append(response.results)
            criteria['older_than'] = response.meta.pagination.older.older

        return pages

    def _get_endpoint_for_integration(self):
        raise NotImplementedError('You must implement this method to return the'
                                 ' desired endpoint. E.g. `self.client.social`')

    def _get_base_data_endpoint(self, name):
        return getattr(self.client, name)
