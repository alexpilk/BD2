from rest_framework import serializers
from .models import RodzajSprzetu


class RodzajeSprzetuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RodzajSprzetu
        fields = '__all__'
