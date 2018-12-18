import re
from operator import and_, or_
from functools import reduce
from django.core.exceptions import FieldError
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend

filter_match_re = re.compile(r'^filter\[([\w\.]+)\](?:\[([\w]+)\])?')


class HotelFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}

        for key, value in request.query_params.items():
            match = filter_match_re.match(key)

            if match is None:
                continue

            field_name, field_lookup = match.groups()
            field_name = field_name.replace('.', '__')

            filter_lookup = field_name
            if field_lookup is not None:
                filter_lookup = '{}__{}'.format(field_name, field_lookup)

            if field_lookup in ('in', 'range'):
                value = value.split(',')

            filters[filter_lookup] = value

        filters = [Q(**{key: value}) for key, value in filters.items()]

        if not filters:
            return queryset

        operator = request.query_params.get('filterOperator', 'and').lower()

        if operator == 'or':
            filters = reduce(or_, filters)
        else:
            filters = reduce(and_, filters)

        try:
            return queryset.filter(filters)
        except FieldError as e:
            raise ValidationError(e)
