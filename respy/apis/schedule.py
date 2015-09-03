from respy.utils import ArgumentConverter


class ScheduleAPI(object):
    """
    Provides an interface for accessing the schedule related endpoints within the reservoir API.
    You should not instantiate this class directly; use the
    :meth:'reservoir.Reservoir.schedule' method instead.
    """

    def __init__(self, client):
        """
        Initializes a new instance of the schedule api using the provided 'client'
        parameter to make HTTP requests.
        :param client: The client in which to make HTTP requests.
        """
        self._client = client
        self._argument_converter = ArgumentConverter()

    def all(self, story, network=None, keyword=None, q=None, older_than=None, newer_than=None,
            limit=None, include_shares=False, order_by='-created_date', include_bounds=False, **kwargs):
        """
        Returns a collection of scheduled content items from a network within the reservoir along with
        any matching meta data.
        :param story: The identifier for the story to retrieve items for.
        :param network: The source social network for the items.
        :param keyword: A keyword that represents the 'feed' that you wish to retrieve. e.g. #GaryIsAwesome
        :param q: A class: 'reservoir.Query' object that indicates the criteria to filter the results by.
        :param older_than: Only fetch scheduled items that are older than this date.
        :param newer_than: Only fetch scheduled items that are newer than this date.
        :param limit: Only fetch this number of social items.
        :param include_shares: Fetch items that have been re-shared, for example Re-Tweets.
        :param order_by: Order the collection by this field, prefix with an '-' to indicate descending direction.
        :param include_bounds: Include the older or newer than ID bound item in the results.
        :return: A collection of scheduled items.
        """

        url = self._build_url(story)
        feeds = None
        if network and keyword:
            network = network.lower()
            feeds = u'{}{}'.format(network, keyword)

        arguments = self._argument_converter(
            feeds=feeds,
            q=q,
            older=older_than,
            since=newer_than,
            limit=limit,
            include_shares=include_shares,
            sort=order_by,
            include_bounds=include_bounds
        )

        return self._client.get(url, **arguments)

    def add(self, story, items_to_schedule):
        """
        Sets items to be scheduled.
        :param story: The story to mark the item as scheduled against.
        :param items_to_schedule: The items to add to the schedule, consisting of ID and the date to publish.
        :return: The scheduled items.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data={
                'items': items_to_schedule
            }
        )

        result = self._client.post(url, **arguments)
        return result

    def delete(self, story, items_to_unschedule):
        """
        Removes items from schedule.
        :param story: The story to remove the scheduled items from.
        :param items_to_unschedule: The items to remove from schedule containing a list of Reservoir Meta IDs or taskIds
        :return: The items removed from the schedule.
        """
        url = self._build_url(story)
        arguments = self._argument_converter(
            data=items_to_unschedule
        )

        result = self._client.delete(url, **arguments)
        return result

    def _build_url(self, story):
        """
        Builds a formatted URL for any of the shortlist end points.
        :param story: The story ID.
        :return: A URL string.
        """
        return u'/api/items/{}/schedule/'.format(story)
