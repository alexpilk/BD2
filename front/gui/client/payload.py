from future.utils import iteritems


class Payload(dict):

    def add_fields(self, fields):
        """
        :param dict fields: e.g.
        ::

            {
                'type': [
                    'field_1',
                    'field_2',
                    'field_3'
                ]
            }

        """
        self.update(
            {
                'fields[{}]'.format(field): ','.join(values) for field, values in iteritems(fields)
            }
        )

    def add_filters(self, filters):
        """
        :param list(Filter) filters: e.g.
        ::

            [
                filter[attribute][contains]=value, ...
            ]

        """
        self.update(
            {
                filter_.key: filter_.value for filter_ in filters
            }
        )

    def add_include(self, include):
        """
        :param list(string) include: e.g.
        ::

            ['relationship_1', 'relationship_2']

        """
        if include:
            self.update(
                {
                    'include': ','.join(include)
                }
            )
