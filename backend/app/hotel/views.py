import inspect

from rest_framework.viewsets import ModelViewSet

from . import serializers


def create_view(serializer):
    class HotelView(ModelViewSet):
        queryset = serializer.Meta.model.objects.all()
        serializer_class = serializer

    return HotelView


views = []

for _, serializer in serializers.__dict__.items():
    if inspect.isclass(serializer) and \
            issubclass(serializer, serializers.HotelSerializer) and \
            serializer != serializers.HotelSerializer:
        views.append(create_view(serializer))
