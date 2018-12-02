from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from .views import RodzajeSprzetuView

router = routers.DefaultRouter()
router.register(r'rodzaje_sprzetu', RodzajeSprzetuView)

urlpatterns = [
    url(r'^', include(router.urls))
]
