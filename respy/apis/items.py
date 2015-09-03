from respy.utils import ArgumentConverter


class ItemsAPI(object):
    """
    Provides an interface for accessing the items related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.items' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the social api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def all(self, story, item_ids):
        """
        Returns a collection of items for the provided item ids.
        :param story: The identifier for the story to retrieve items for.
        :param item_ids: Return the information for these item ID's.
        :return: A collection of items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            ids=item_ids
        )

        return self._client.get(url, **arguments)

    def _build_url(self, story):
        """
        Builds a formatted URL for any of the social end points.
        :param story: The story ID.
        :return: A URL string.
        """
        return u'/api/items/{}/'.format(story)