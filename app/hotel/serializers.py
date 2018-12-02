from rest_framework import serializers
from .models import RodzajeSprzetu


class RodzajeSprzetuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RodzajeSprzetu
        fields = '__all__'
