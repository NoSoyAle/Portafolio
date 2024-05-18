from django.urls import path
from .views import home, iniciosesion, crearcuenta

urlpatterns = [
    path('', home, name="home"),
    path('iniciosesion/', iniciosesion, name="iniciarsesion"),
    path('crearcuenta/', crearcuenta, name='crearcuenta'),
]