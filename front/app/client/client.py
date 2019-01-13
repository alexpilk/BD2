import logging
from pprint import pformat

import requests
import urllib3

from .json_api_doc import parse
from .payload import Payload
from .filters import create_filters

logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)  # this is necessary

urllib3.disable_warnings()


class ResponseWrapper(dict):

    def __repr__(self):
        return pformat(dict(self))


class ApiError(Exception):
    pass


class ApiClient(object):

    def __init__(self, api_root):
        self.api_url = api_root

    def get(self, endpoint, fields=None, filters=None, include=None):
        """
        Example usage:
        ::

            client.get(
                endpoint='netacts',
                fields={
                    'netact': [
                        'was_host',
                        'was_ssh_user',
                        'omses',
                        'ip'
                    ]
                },
                filters={
                    'ip': '10.92.96.57'
                },
                include=['omses']
            )

        :param string endpoint:
        :param dict(string, list) fields:
        :param dict filters:
        :param list include:
        :return: API response
        :rtype: ResponseWrapper
        """
        url = self._build_url(endpoint)
        payload = self._build_payload(fields=fields, filters=filters, include=include)
        return self._get_request(url, payload=payload)

    def _post_or_update(self, method, endpoint, attributes, relationships=None, _id=None):
        relationships = relationships or {}
        url = self._build_url(endpoint) + (f'/{_id}' if _id else '')
        payload = {
            "data": {
                "type": endpoint,
                "attributes": attributes,
                "relationships": {
                    attribute: {
                        "data": {
                            "type": value['type'],
                            "id": value['id']
                        }
                    }
                for attribute, value in relationships.items()}
            }
        }
        if _id:
            payload['data']['id'] = _id
        return self._post_request(method, url, payload=payload)[0]

    def create(self, endpoint, attributes, relationships=None):
        return self._post_or_update('post', endpoint, attributes, relationships)

    def update(self, endpoint, _id, attributes, relationships=None):
        return self._post_or_update('patch', endpoint, attributes, relationships, _id=_id)

    def delete(self, endpoint, _id):
        url = self._build_url(endpoint) + f'/{_id}'
        requests.delete(url)
        logger.debug(f'Deleted {endpoint} {_id}')

    @staticmethod
    def _parse_response(response):
        if 'errors' in response:
            raise ApiError('\n'.join(error['detail'] for error in response['errors']))
        parsed_response = parse(response)
        return [ResponseWrapper(item) for item in parsed_response]

    def _build_url(self, endpoint):
        return '{url}{endpoint}'.format(url=self.api_url, endpoint=endpoint)

    @staticmethod
    def _build_payload(fields=None, filters=None, include=None):
        payload = Payload()
        payload.add_fields(fields or {})
        payload.add_include(include or [])
        payload.add_filters(create_filters(filters or {}))
        logger.debug('Built request:\n{}'.format(pformat(payload)))
        return payload

    def _get_request(self, url, payload):
        response = requests.get(url, params=payload).json()
        parsed_response = self._parse_response(response)
        logger.debug('Received response:\n{}'.format(parsed_response))
        return parsed_response

    def _post_request(self, method, url, payload=None):
        payload = payload or {}
        response = requests.request(method, url + '/', json=payload,
                                    headers={'Content-type': 'application/vnd.api+json'}).json()
        parsed_response = self._parse_response(response)
        logger.debug('Received response:\n{}'.format(parsed_response))
        return parsed_response
