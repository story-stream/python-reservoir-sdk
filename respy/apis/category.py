from respy.utils import ArgumentConverter


class CategoryAPI(object):
    """
    Provides an interface for accessing the category related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.category' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the shortlist api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def add(self, story, item_ids, category):
        """
        Categorises a list of items against a specified category.
        :param story: The story the items are associated with.
        :param item_ids: Categorise these item ID's.
        :param category: The category to use.
        :return: The categorised items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids,
                'category': category
            }
        )

        result = self._client.post(url, **arguments)
        return result

    def delete(self, story, item_ids, category):
        """
        Removes a category from a list of items.
        :param story: The story the items are associated with.
        :param item_ids: The item ID's to remove the category from.
        :param category: The category to remove.
        :return: The affected items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids,
                'category': category
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
        return u'/api/items/{}/category/'.format(story)
