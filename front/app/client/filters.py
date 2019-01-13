def create_filters(filters, prefix=None, operator=None):
    """
    Helper function for generating filters.

    :param dict filters: e.g. {'attribute': 'value'}
    :param prefix: required when filtering by attributes of related objects e.g. 'attribute'
    :param operator: JSON API filter operator e.g. 'contains'
    :return: filters
    :rtype: list(Filter)
    """
    return [
        Filter(
            '{}.{}'.format(prefix, attribute) if prefix else attribute,
            value,
            operator
        ) for attribute, value in filters.items()
    ]


class Filter(object):

    def __init__(self, attribute, value, operator=None):
        self.attribute = attribute
        self.value = value
        self.operator = operator or ''

    @property
    def key(self):
        """
        :return: filter key e.g. 'filter[relationship.attribute][contains]'
        :rtype: string
        """
        return f'filter[{self.attribute}]' + (f'[{self.operator}]' if self.operator else '')

    def __repr__(self):
        return '{key}={value}'.format(
            key=self.key, value=self.value
        )
