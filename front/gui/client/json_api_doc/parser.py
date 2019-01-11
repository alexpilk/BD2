from future.utils import iteritems
from .flattener import flatten
from .includes import IncludesWrapper


def parse(content):
    """
    :param dict content: raw JSON API document
    :return: parsed JSON API document
    :rtype: dict
    """
    return Parser(content).parse()


class Parser(object):

    def __init__(self, document):
        primary_members = ('data', 'errors', 'meta')
        if all(member not in document for member in primary_members):
            raise AttributeError('This is not a JSON API document')
        data, included = document.get('data'), document.get('included')
        self.data = self._prepare_data(data or [])
        self.included = self._prepare_included(included or {})

    @staticmethod
    def _prepare_data(data):
        if isinstance(data, dict):
            data = [data]
        return [flatten(item) for item in data]

    @staticmethod
    def _prepare_included(included):
        return IncludesWrapper(included)

    def parse(self):
        """
        :return: parsed JSON API document
        """
        return [self._resolve(item) for item in self.data]

    def _resolve(self, data):
        return {
            attribute_name: self._parse_attribute(attribute_value) for attribute_name, attribute_value in iteritems(data)
        }

    def _parse_attribute(self, attribute_value):
        if isinstance(attribute_value, list):
            return [
                self._resolve_if_relationship(item) for item in attribute_value
            ]
        return self._resolve_if_relationship(attribute_value)

    def _resolve_if_relationship(self, attribute_value):
        if isinstance(attribute_value, tuple):
            relationship = self.included.get(attribute_value)
            return self._resolve(relationship)
        return attribute_value
