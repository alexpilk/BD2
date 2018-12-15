from rest_framework import viewsets, serializers
from .serializers import RodzajeSprzetuSerializer
from . import models
import inspect
from django.db.models import Model


# class RodzajeSprzetuView(viewsets.ModelViewSet):
#     queryset = RodzajSprzetu.objects.all()
#     serializer_class = RodzajeSprzetuSerializer


def create_view(base_model):
    class HotelSerializer(serializers.ModelSerializer):
        class Meta:
            model = base_model
            fields = '__all__'

    class HotelView(viewsets.ModelViewSet):
        queryset = base_model.objects.all()
        serializer_class = HotelSerializer

    return HotelView


views = []


for _, model in models.__dict__.items():
    if inspect.isclass(model) and issubclass(model, Model):
        views.append(create_view(model))

