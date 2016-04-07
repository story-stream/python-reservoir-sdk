from apis import (
    BrandAPI,
    CategoryAPI,
    ItemsAPI,
    PublishAPI,
    ScheduleAPI,
    SocialAPI,
    ShortlistAPI,
    TagAPI,
)

from client import Client


class Reservoir(object):
    """
    Main entry point for accessing the Reservoir API.

    Essentially this is a factory calls that creates various instances of classes
    that can be used to communicate to endpoints within the Reservoir infrastructure.
    """

    def __init__(self, access_token=None, base_url=None):
        """
        Initializes a new Reservoir instance.
        :param access_token: The access token which has been assigned for the application
        to communicate with the reservoir.
        :param base_url: Defaults to the live Reservoir API. Provide another value to make requests
        to another URL. e.g. a fake in your applications test suite.
        """
        self._access_token = access_token
        self._brand_api = None
        self._category_api = None
        self._client = Client(
            access_token=access_token,
            base_url=base_url
        )
        self._items_api = None
        self._publish_api = None
        self._schedule_api = None
        self._shortlist_api = None
        self._social_api = None
        self._tag_api = None

    @property
    def brand(self):
        """
        Returns a :class:'reservoir.apis.BrandAPI' object which can be used to call
        the Reservoir API's brand related endpoints.
        :return: A reservoir brand api object
        """
        if not self._brand_api:
            self._brand_api = BrandAPI(client=self._client)

        return self._brand_api

    @property
    def category(self):
        """
        Returns a :class:'reservoir.apis.CategoryAPI' object which can be used to call
        the Reservoir API's category related endpoints.
        :return: A reservoir category api object
        """
        if not self._category_api:
            self._category_api = CategoryAPI(client=self._client)

        return self._category_api

    @property
    def client(self):
        """
        Returns a :class 'reservoir.client.Client' object which can be used to make
        HTTP requests to the Reservoir REST API endpoints.

        You should only use this if there isn't a more specific interface available
        for the request you wish to make.
        :return: A reservoir client object.
        """
        return self._client

    @property
    def items(self):
        """
        Returns a :class:'reservoir.apis.ItemsAPI' object which can be used to call
        the Reservoir API's items related endpoints.
        :return: A reservoir items api object
        """
        if not self._items_api:
            self._items_api = ItemsAPI(client=self._client)

        return self._items_api

    @property
    def publish(self):
        """
        Returns a :class:'reservoir.apis.PublishAPI' object which can be used to call
        the Reservoir API's publish related endpoints.
        :return: A reservoir publish api object
        """
        if not self._publish_api:
            self._publish_api = PublishAPI(client=self._client)

        return self._publish_api

    @property
    def schedule(self):
        """
        Returns a :class:'reservoir.apis.ScheduleAPI' object which can be used to call
        the Reservoir API's schedule related endpoints.
        :return: A reservoir schedule api object
        """
        if not self._schedule_api:
            self._schedule_api = ScheduleAPI(client=self._client)

        return self._schedule_api

    @property
    def shortlist(self):
        """
        Returns a :class:'reservoir.apis.ShortlistAPI' object which can be used to call
        the Reservoir API's shortlist related endpoints.
        :return: A reservoir shortlist api object
        """
        if not self._shortlist_api:
            self._shortlist_api = ShortlistAPI(client=self._client)

        return self._shortlist_api

    @property
    def social(self):
        """
        Returns a :class:'reservoir.apis.SocialAPI' object which can be used to call
        the Reservoir API's social related endpoints.
        :return: A reservoir social api object
        """
        if not self._social_api:
            self._social_api = SocialAPI(client=self._client)

        return self._social_api

    @property
    def tag(self):
        """
        Returns a :class:'reservoir.apis.TagAPI' object which can be used to call
        the Reservoir API's tag related endpoints.
        :return: A reservoir tag api object
        """
        if not self._tag_api:
            self._tag_api = TagAPI(client=self._client)

        return self._tag_api
