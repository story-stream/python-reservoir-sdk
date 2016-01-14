from respy.utils import ArgumentConverter


class SocialAPI(object):
    """
    Provides an interface for accessing the social related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.social' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the social api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def all(self, story, feeds, q=None, categories=None, tags=None,
            older_than=None, newer_than=None, limit=None, include_shares=False,
            order_by='-created_date', include_bounds=False, **kwargs):
        """
        Returns a collection of social content items from a network within the reservoir along with
        any matching meta data.
        :param story: The identifier for the story to retrieve items for.
        :param feeds: List of dictionary objects with format {type:"network", search:"term"} e.g. [{type:twitter, search:"#storystream"}].
        :param q: A class: 'reservoir.Query' object that indicates the criteria to filter the results by.
        :param categories: list of strings containing categories to filter by
        :param tags: list of strings containing tags to filter by
        :param older_than: Only fetch social items that are older than this date.
        :param newer_than: Only fetch social items that are newer than this date.
        :param limit: Only fetch this number of social items.
        :param include_shares: Fetch items that have been re-shared, for example Re-Tweets.
        :param order_by: Order the collection by this field, prefix with an '-' to indicate descending direction.
        :param include_bounds: Include the older or newer than ID bound item in the results.
        :return: A collection of social items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            feeds=feeds,
            q=q,
            categories=categories,
            tags=tags,
            older=older_than,
            since=newer_than,
            limit=limit,
            include_shares=include_shares,
            sort=order_by,
            include_bounds=include_bounds
        )

        return self._client.get(url, **arguments)

    def delete(self, story, item_ids):
        """
        Marks items as deleted from a story which prevents them from showing when calling
        :meth:'respy.apis.SocialAPI.all'.
        :param story: The story to mark the items as deleted for.
        :param item_ids: Delete these item ID's
        :return: A collection of items that have been deleted.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids
            }
        )
        return self._client.delete(url, **arguments)

    def _build_url(self, story):
        """
        Builds a formatted URL for any of the social end points.
        :param story: The story ID.
        :return: A URL string.
        """
        return u'/api/items/{}/social/'.format(story)
