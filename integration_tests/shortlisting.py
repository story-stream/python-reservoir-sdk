from base_integration import BaseIntegration


class ShortlistIntegration(BaseIntegration):
    def _get_endpoint_for_integration(self):
        return self.client.shortlist

    def setUp(self):
        super(ShortlistIntegration, self).setUp()
        self.story_id = 1

    def test_can_return_correct_number_of_items_when_providing_a_limit(self):
        social_items = self.get_only_keys(self.story_id,
                                          '_id',
                                          endpoint='social')

        social_ids = [i['_id'] for i in social_items]

        self._reverse_on_tear_down(self.client.shortlist.add,
                                  self.story_id,
                                  social_ids)

        limited_shortlisted_items = self.get_only_keys(self.story_id,
                                                       '_id',
                                                       limit=2)

        self.assertEqual(len(limited_shortlisted_items), 2)

    def test_item_is_removed_from_social_when_added_to_shortlist(self):
        social_ids = self.get_only_keys(self.story_id,
                                        '_id',
                                        endpoint='social')

        first_item = social_ids[0]['_id']

        self.assertFalse(self.get_only_keys(self.story_id, '_id'))
        self._reverse_on_tear_down(self.client.shortlist.add,
                                  self.story_id, [first_item])

        updated_social_ids = self.get_only_keys(self.story_id,
                                                '_id',
                                                endpoint='social')

        self.assertNotIn({'_id': first_item}, updated_social_ids)

    def test_item_is_added_to_shortlist(self):
        social_ids = self.get_only_keys(self.story_id,
                                        '_id',
                                        endpoint='social')

        first_item = social_ids[0]['_id']

        self.assertFalse(self.get_only_keys(self.story_id, '_id'))
        self._reverse_on_tear_down(self.client.shortlist.add, self.story_id, [first_item])

        updated_shortlist_ids = self.get_only_keys(self.story_id, '_id')

        self.assertIn({'_id': first_item}, updated_shortlist_ids)

    def test_can_return_items_filtered_by_category(self):
        social_items = self.get_only_keys(self.story_id,
                                          '_id',
                                          endpoint='social')

        social_ids = [i['_id'] for i in social_items]

        self._reverse_on_tear_down(self.client.shortlist.add, self.story_id, social_ids)

        # add category
        self._reverse_on_tear_down(self.client.category.add, self.story_id, social_ids[:5], 'test-cat')

        # filter by category
        filtered_items = self.get_only_keys(self.story_id,
                                            '_id',
                                            categories=['test-cat'])

        self.assertEqual(len(filtered_items), 5)

    def test_can_paginate_through_older_items(self):
        social_items = self.get_only_keys(self.story_id,
                                        '_id',
                                        endpoint='social',
                                        limit=50)

        social_ids = [i['_id'] for i in social_items]

        self._reverse_on_tear_down(self.client.shortlist.add, self.story_id, social_ids)

        shortlisted_items = self.get_only_keys(self.story_id, limit=50)
        self.assertEqual(len(shortlisted_items.results), 50)

        expected_pages = []
        for i in range(0, 10):
            page = shortlisted_items.results[i*5:(i*5)+5]
            expected_pages.append([{'_id': item._id} for item in page])

        actual_pages = self.traverse_older_pages(self.story_id,
                                                 limit=5,
                                                 number_of_pages=10)

        for i in range(0, len(expected_pages)):
            page = expected_pages[i]
            for j in range(0, len(page)):
                self.assertEqual(page[j]['_id'], actual_pages[i][j]['_id'])

    def test_can_paginate_through_older_items_and_back_up(self):
        social_items = self.get_only_keys(self.story_id,
                                          '_id',
                                          endpoint='social',
                                          limit=20)

        social_ids = [i['_id'] for i in social_items]

        self._reverse_on_tear_down(self.client.shortlist.add, self.story_id, social_ids)

        shortlisted_items = self.get_only_keys(self.story_id, limit=20)
        self.assertEqual(len(shortlisted_items.results), 20)

        expected_pages = []
        for i in range(0, 10):
            page = shortlisted_items.results[i*5:(i*5)+5]
            if page:
                expected_pages.append(page)

        # now lets go back up from the start of the last page
        since = expected_pages[-1][0]
        reverse_pages = self.traverse_newer_pages(self.story_id,
                                                  number_of_pages=4,
                                                  newer_than=since['timestamp'])

        def compare(expected, actual):
            for i in range(0, len(expected)):
                self.assertEqual(expected[i]['_id'], actual[i]['_id'])

        compare(expected_pages[-2], reverse_pages[0])
        compare(expected_pages[-3], reverse_pages[1])
        compare(expected_pages[-4], reverse_pages[2])
