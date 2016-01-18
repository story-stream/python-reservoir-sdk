from respy.utils import ArgumentConverter


class ShortlistAPI(object):
    """
    Provides an interface for accessing the shortlist related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.shortlist' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the shortlist api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def all(self, story, feeds, q=None, categories=None, tags=None,
            older_than=None, newer_than=None, limit=None, include_shares=False,
            order_by='-timestamp', include_bounds=False, **kwargs):
        """
        Returns a collection of shortlisted content items from a network within the reservoir along with
        any matching meta data.
        :param story: The identifier for the story to retrieve items for.
        :param feeds: List of dictionary objects with format {type:"network", search:"term"} e.g. [{type:twitter, search:"#storystream"}].
        :param q: A class: 'reservoir.Query' object that indicates the criteria to filter the results by.
        :param categories: list of strings containing categories to filter by
        :param tags: list of strings containing tags to filter by
        :param older_than: Only fetch shortlisted items that are older than this date.
        :param newer_than: Only fetch shortlisted items that are newer than this date.
        :param limit: Only fetch this number of social items.
        :param include_shares: Fetch items that have been re-shared, for example Re-Tweets.
        :param order_by: Order the collection by this field, prefix with an '-' to indicate descending direction.
        :param include_bounds: Include the older or newer than ID bound item in the results.
        :return: A collection of shortlisted items.
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

    def add(self, story, item_ids):
        """
        Sets items to be shortlisted.
        :param story: The story to mark the item as shortlisted against.
        :param item_ids: Shortlist these items.
        :return: The shortlisted items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids
            }
        )

        result = self._client.post(url, **arguments)
        return result

    def delete(self, story, item_ids):
        """
        Removes items from shortlisted.
        :param story: The story to remove the shortlisted items from.
        :param item_id: Remove shortlist from these items.
        :return: The un-shortlisted items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'ids': item_ids
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
        return u'/api/items/{}/shortlist/'.format(story)
