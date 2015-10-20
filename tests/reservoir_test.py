from unittest import TestCase
from mock import patch, Mock

from respy import Reservoir
from respy.client import Client
from respy.reservoir import (
    CategoryAPI,
    ItemsAPI,
    PublishAPI,
    ScheduleAPI,
    ShortlistAPI,
    SocialAPI,
    TagAPI,
)


class ReservoirTest(TestCase):

    @patch('respy.reservoir.CategoryAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_category_returns_a_category_api_instance(self, MockClient, MockCategoryAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        category = reservoir.category

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockCategoryAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(category, CategoryAPI)

    @patch('respy.reservoir.ItemsAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_items_returns_a_items_api_instance(self, MockClient, MockItemsAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        items = reservoir.items

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockItemsAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(items, ItemsAPI)

    @patch('respy.reservoir.PublishAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_publish_returns_a_publish_api_instance(self, MockClient, MockPublishAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        publish = reservoir.publish

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockPublishAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(publish, PublishAPI)

    @patch('respy.reservoir.ScheduleAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_schedule_returns_a_schedule_api_instance(self, MockClient, MockScheduleAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        schedule = reservoir.schedule

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockScheduleAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(schedule, ScheduleAPI)

    @patch('respy.reservoir.ShortlistAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_shortlist_returns_a_shortlist_api_instance(self, MockClient, MockShortlistAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        shortlist = reservoir.shortlist

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockShortlistAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(shortlist, ShortlistAPI)

    @patch('respy.reservoir.SocialAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_social_returns_a_social_api_instance(self, MockClient, MockSocialAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        social = reservoir.social

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockSocialAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(social, SocialAPI)

    @patch('respy.reservoir.TagAPI', spec=True)
    @patch('respy.reservoir.Client', spec=True)
    def test_tag_returns_a_tag_api_instance(self, MockClient, MockTagAPI):
        reservoir = Reservoir(
            access_token='zxy',
            base_url='123'
        )
        tag = reservoir.tag

        MockClient.assert_called_once_with(
            access_token='zxy',
            base_url='123'
        )
        MockTagAPI.assert_called_once_with(
            client=MockClient()
        )
        self.assertIsInstance(tag, TagAPI)

    @patch('respy.reservoir.Client', spec=True)
    def test_client_returns_a_client_instance(self, MockClient):
        reservoir = Reservoir(
            access_token='abc123',
            base_url='http://testing.site'
        )
        client = reservoir.client

        MockClient.assert_called_once_with(
            access_token='abc123',
            base_url='http://testing.site'
        )

        self.assertIsInstance(client, Client)
