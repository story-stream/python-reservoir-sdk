from __future__ import division
from datetime import datetime, timedelta
from base_test_case import BaseTestCase


class PublishItemTestCase(BaseTestCase):
    def setUp(self):
        super(PublishItemTestCase, self).setUp()
        self.story_id = 1
    
    def test_can_publish_an_item_from_shortlisted(self):
        self.assertEqual(1, 2)

    def test_can_publish_an_item_which_hasnt_been_touched(self):
        items = self._get_social('_id')
        social_item = items[0]['_id']

        self.client.publish.add(self.story_id, [{
            'id': social_item,
            'date': self.__totimestamp(datetime.utcnow())
        }])

        updated_published = self.client.items.all(self.story_id, [social_item])
        self.assertEqual(len(updated_published.results), 1)

        pub_item = updated_published.results[0]

        self.assertEqual(pub_item['_id'], social_item)
        self.assertEqual(pub_item.meta['is_published'], True)

    def test_can_publish_and_item_which_was_scheduled(self):
        self.assertEqual(1, 2)

    def test_can_unpublish_item(self):
        items = self._get_social('_id')
        social_item = items[0]['_id']

        self.client.publish.add(self.story_id, [{
            'id': social_item,
            'date': self.__totimestamp(datetime.utcnow())
        }])

        updated_published = self.client.items.all(self.story_id, [social_item])
        self.assertEqual(len(updated_published.results), 1)

        self.client.publish.delete(self.story_id, [{
            'id': social_item,
            'date': self.__totimestamp(datetime.utcnow())
        }])

        updated_published = self.client.items.all(self.story_id, [social_item])
        pub_item = updated_published.results[0]

        self.assertEqual(pub_item['_id'], social_item)
        self.assertEqual(pub_item.meta['is_published'], False)

    def _get_social(self, *keys, **kwargs):
        response = self.client.social.all(self.story_id, [
            {'type': 'twitter', 'search': '#bluemonday'}
        ], **kwargs)
        return self.parser.extract_data(response, *keys)

    def _get_shortlist(self, *keys, **kwargs):
        response = self.client.shortlist.all(self.story_id, [
            {'type': 'twitter', 'search': '#bluemonday'}
        ], **kwargs)
        return self.parser.extract_data(response, *keys)

    def _get_published(self, *keys, **kwargs):
        response = self.client.publish.all(self.story_id, [
            {'type': 'twitter', 'search': '#bluemonday'}
        ], **kwargs)
        return self.parser.extract_data(response, *keys)

    def __totimestamp(self, dt, epoch=datetime(1970,1,1)):
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
