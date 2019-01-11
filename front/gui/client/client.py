import logging
from pprint import pformat

import requests
import urllib3
from attrdict import AttrDict

from .json_api_doc import parse
from .payload import Payload

logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)  # this is necessary

urllib3.disable_warnings()


class ResponseWrapper(AttrDict):

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
        response = self._request(url, payload=payload)
        if 'errors' in response:
            raise ApiError('\n'.join(error['detail'] for error in response['errors']))
        parsed_response = self._parse_response(response)
        logger.debug('Received response:\n{}'.format(parsed_response))
        return parsed_response

    @staticmethod
    def _parse_response(response):
        parsed_response = parse(response)
        return [ResponseWrapper(item) for item in parsed_response]

    def _build_url(self, endpoint):
        return '{url}{endpoint}'.format(url=self.api_url, endpoint=endpoint)

    @staticmethod
    def _build_payload(fields=None, filters=None, include=None):
        payload = Payload()
        payload.add_fields(fields or {})
        payload.add_include(include or [])
        payload.add_filters(filters or {})
        logger.debug('Built request:\n{}'.format(pformat(payload)))
        return payload

    @staticmethod
    def _request(url, payload):
        return requests.get(url, params=payload).json()
