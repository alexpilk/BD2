from rest_framework import serializers
from .models import RodzajSprzetu


class RodzajeSprzetuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RodzajSprzetu
        fields = '__all__'


def create_serializer(base_model):
    class HotelSerializer(serializers.ModelSerializer):
        class Meta:
            model = base_model
            fields = '__all__'
    return HotelSerializer


