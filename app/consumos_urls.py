from django.urls import path
from . import views

urlpatterns = [
    path('', views.consumo_index, name='consumo'),
    path('view/<int:id>', views.consumo_view, name='consumo_view'),
    path('edit/<int:id>', views.consumo_edit, name='consumo_edit'),
    path('add/', views.consumo_add, name='consumo_add'),
    path('delete/<int:id>', views.consumo_delete, name='consumo_delete'),
    path('confirm_delete/<int:id>/', views.consumo_confirm_delete, name='consumo_confirm_delete'),
]