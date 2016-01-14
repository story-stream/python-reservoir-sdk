from base_test_case import BaseTestCase


class ShortlistItemTestCase(BaseTestCase):
    def setUp(self):
        super(ShortlistItemTestCase, self).setUp()
        self.steps_to_undo = []
        self.story_id = 1

    def tearDown(self):
        if self.steps_to_undo:
            self.client.shortlist.delete(self.story_id, self.steps_to_undo)

    def test_item_is_removed_from_social_when_added_to_shortlist(self):
        social_ids = self._get_social()
        first_item = social_ids[0]['_id']
        self.steps_to_undo.append(first_item)

        self.assertFalse(self._get_shortlist())
        self.client.shortlist.add(self.story_id, [first_item])

        updated_social_ids = self._get_social()

        self.assertNotIn({'_id': first_item}, updated_social_ids)

    def test_item_is_added_to_shortlist(self):
        social_ids = self._get_social()
        first_item = social_ids[0]['_id']
        self.steps_to_undo.append(first_item)

        self.assertFalse(self._get_shortlist())
        self.client.shortlist.add(self.story_id, [first_item])

        updated_shortlist_ids = self._get_shortlist()

        self.assertIn({'_id': first_item}, updated_shortlist_ids)


    def _get_social(self):
        response = self.client.social.all(self.story_id, [
            {'type': 'twitter', 'search': '#prayforjakarta'}
        ])
        return self.parser.extract_data(response, '_id')

    def _get_shortlist(self):
        response = self.client.shortlist.all(self.story_id, [
            {'type': 'twitter', 'search': '#prayforjakarta'}
        ])
        return self.parser.extract_data(response, '_id')
