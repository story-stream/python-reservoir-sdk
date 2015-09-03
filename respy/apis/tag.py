from respy.utils import ArgumentConverter


class TagAPI(object):
    """
    Provides an interface for accessing the tag related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.tag' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the shortlist api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def add(self, story, item_ids, tag):
        """
        Categorises a list of items against a specified tag.
        :param story: The story the items are associated with.
        :param item_ids: Categorise these item ID's.
        :param tag: The tag to use.
        :return: The categorised items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids,
                'tag': tag
            }
        )

        result = self._client.post(url, **arguments)
        return result

    def delete(self, story, item_ids, tag):
        """
        Removes a tag from a list of items.
        :param story: The story the items are associated with.
        :param item_ids: The item ID's to remove the tag from.
        :param tag: The tag to remove.
        :return: The affected items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids,
                'tag': tag
            }
        )

        result = self._client.delete(url, **arguments)
        return result

    def _build_url(self, story):
        """
        Builds a formatted URL for any of the shortlist end points.
        :param story: The story ID.
        :return: A URL string.
        """
        return u'/api/items/{}/tag/'.format(story)
