from base_test_case import BaseTestCase


class ShortlistItemTestCase(BaseTestCase):
    def setUp(self):
        super(ShortlistItemTestCase, self).setUp()
        self.story_id = 1

    def test_can_return_correct_number_of_items_when_providing_a_limit(self):
        social_items = self._get_social()
        social_ids = [i['_id'] for i in social_items]

        self.reverse_on_tear_down(self.client.shortlist.add,
                                  self.story_id,
                                  social_ids)

        limited_shortlisted_items = self._get_shortlist(limit=2)

        self.assertEqual(len(limited_shortlisted_items), 2)

    def test_item_is_removed_from_social_when_added_to_shortlist(self):
        social_ids = self._get_social()
        first_item = social_ids[0]['_id']

        self.assertFalse(self._get_shortlist())
        self.reverse_on_tear_down(self.client.shortlist.add,
                                  self.story_id, [first_item])

        updated_social_ids = self._get_social()

        self.assertNotIn({'_id': first_item}, updated_social_ids)

    def test_item_is_added_to_shortlist(self):
        social_ids = self._get_social()
        first_item = social_ids[0]['_id']

        self.assertFalse(self._get_shortlist())
        self.reverse_on_tear_down(self.client.shortlist.add, self.story_id, [first_item])

        updated_shortlist_ids = self._get_shortlist()

        self.assertIn({'_id': first_item}, updated_shortlist_ids)

    def test_can_return_items_filtered_by_category(self):
        social_items = self._get_social()
        social_ids = [i['_id'] for i in social_items]

        self.reverse_on_tear_down(self.client.shortlist.add, self.story_id, social_ids)

        # add category
        self.reverse_on_tear_down(self.client.category.add, self.story_id, social_ids[:5], 'test-cat')

        # filter by category
        filtered_items = self._get_shortlist(categories=['test-cat'])
        self.assertEqual(len(filtered_items), 5)

    def _get_social(self, **kwargs):
        response = self.client.social.all(self.story_id, [
            {'type': 'twitter', 'search': '#prayforjakarta'}
        ], **kwargs)
        return self.parser.extract_data(response, '_id')

    def _get_shortlist(self, **kwargs):
        response = self.client.shortlist.all(self.story_id, [
            {'type': 'twitter', 'search': '#prayforjakarta'}
        ], **kwargs)
        return self.parser.extract_data(response, '_id')
