from base_integration import BaseIntegration


class SocialIntegration(BaseIntegration):
    def _get_endpoint_for_integration(self):
        return self.client.social

    def setUp(self):
        super(SocialIntegration, self).setUp()
        self.story_id = 1

    def test_can_return_correct_number_of_items_when_providing_a_limit(self):
        limited_social_items = self.get_only_keys(self.story_id, '_id', limit=2)

        self.assertEqual(len(limited_social_items), 2)

    def test_can_paginate_through_older_items(self):
        social_items = self.get_full(self.story_id, limit=50)

        expected_pages = []
        for i in range(0, 10):
            page = social_items.results[i*5:(i*5)+5]
            expected_pages.append([{'_id': item._id} for item in page])

        def get_paged_data(max_iterations):
            pages = []
            kwargs = {'limit': 5}
            has_ended = False
            total = 0
            while not has_ended and total < max_iterations:
                total += 1
                resp = self._get_social(**kwargs)
                if resp.results:
                    pages.append([{'_id': i['_id']} for i in resp.results])
                    kwargs['older_than'] = resp.meta.pagination.older.older
                else:
                    has_ended = True
            return pages

        actual_pages = self.traverse_older_pages(self.story_id,
                                                 limit=5,
                                                 number_of_pages=10)

        self.assertEqual(len(expected_pages), len(actual_pages))

        for i in range(0, len(expected_pages)):
            page = expected_pages[i]
            for j in range(0, len(page)):
                self.assertEqual(page[j]['_id'], actual_pages[i][j]['_id'])

    def test_can_paginate_through_older_items_and_back_up(self):
        social_items = self.get_full(self.story_id, limit=20)

        expected_pages = []
        for i in range(0, 4):
            page = social_items.results[i*5:(i*5)+5]
            if page:
                expected_pages.append(page)

        older_pages = self.traverse_older_pages(self.story_id,
                                                limit=5,
                                                number_of_pages=4)

        # now lets go back up from the start of the last page
        since = expected_pages[-1][0]
        reverse_pages = self.traverse_newer_pages(self.story_id,
                                                  limit=5,
                                                  number_of_pages=4,
                                                  newer_than=since['timestamp'])

        def compare(expected, actual):
            for i in range(0, len(expected)):
                self.assertEqual(expected[i]['_id'], actual[i]['_id'])

        self.assertEqual(len(expected_pages)-1, len(reverse_pages))

        compare(expected_pages[-4], reverse_pages[2])
        compare(expected_pages[-3], reverse_pages[1])
        compare(expected_pages[-2], reverse_pages[0])

    def test_can_return_items_filtered_by_category(self):
        social_items = self.get_only_keys(self.story_id, '_id')
        social_ids = [i['_id'] for i in social_items]
        # add category
        self._reverse_on_tear_down(self.client.category.add,
                                    self.story_id,
                                    social_ids[:5],
                                    'test-cat')
        # filter by category
        filtered_items = self.get_only_keys(self.story_id,
                                            '_id',
                                            categories=['test-cat'])

        self.assertEqual(len(filtered_items), 5)
