from future.utils import iteritems
from .relationships import relationship_to_tuple


def flatten(obj):
    """
    Removes unneeded data, parses attributes and relationships.
    """
    _delete_links(obj)
    _collect_attributes(obj)
    _collect_relationships(obj)
    return obj


def _delete_links(obj):
    obj.pop('links', None)


def _collect_attributes(obj):
    attributes = obj.pop('attributes', {})
    obj.update(attributes)


def _collect_relationships(obj):
    relationships = obj.pop('relationships', {})
    for name, content in iteritems(relationships):
        obj[name] = _parse_relationships(content['data'])


def _parse_relationships(data):
    if isinstance(data, list):
        return [
            relationship_to_tuple(relationship) for relationship in data
        ]
    elif isinstance(data, dict):
        return relationship_to_tuple(data)
