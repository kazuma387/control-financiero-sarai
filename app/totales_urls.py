from django.urls import path
from . import views

urlpatterns = [
    path('total-costos/', views.total_costos, name='total_costos'),
]