from rest_framework import viewsets
from .models import RodzajeSprzetu
from .serializers import RodzajeSprzetuSerializer


class RodzajeSprzetuView(viewsets.ModelViewSet):
    queryset = RodzajeSprzetu.objects.all()
    serializer_class = RodzajeSprzetuSerializer
