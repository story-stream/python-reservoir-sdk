from constants import ARGUMENT_CONVERTED_KEY


class ArgumentConverter(object):
    """
    A callable object that takes a dict (in the form of keyword arguments),
    sanitises it and returns the result.
    """

    def __call__(self, **kwargs):
        """
        Formats a dict of keyword arguments and returns the result.
        """
        converted_args = kwargs.copy()
        for key, value in kwargs.iteritems():
            if value is None:
                del converted_args[key]

            formatted_key = key.replace('_', '-')
            if '_' in key:
                del converted_args[key]
                converted_args[formatted_key] = value

            # if isinstance(value, bool):
            #     converted_args[formatted_key] = str(value).lower()

            if key == 'q' and value:
                if isinstance(value, list):
                    converted_args[formatted_key] = ' OR '.join(value)
                else:
                    converted_args[formatted_key] = value

            if key == 'ids' and value:
                converted_args[formatted_key] = value #','.join([str(item_id) for item_id in value])

        converted_args[ARGUMENT_CONVERTED_KEY] = True

        return converted_args
