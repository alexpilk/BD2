from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from .views import views

router = routers.DefaultRouter()
# router.register(r'rodzaje_sprzetu', RodzajeSprzetuView)
for view in views:
    router.register(view.serializer_class.Meta.model.__name__, view)


urlpatterns = [
    url(r'^', include(router.urls))
]
