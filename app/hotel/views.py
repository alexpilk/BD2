from rest_framework import viewsets
from .models import RodzajSprzetu
from .serializers import RodzajeSprzetuSerializer


class RodzajeSprzetuView(viewsets.ModelViewSet):
    queryset = RodzajSprzetu.objects.all()
    serializer_class = RodzajeSprzetuSerializer
