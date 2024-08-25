from django.urls import path
from . import views

urlpatterns = [
    path('', views.paciente_index, name='paciente'),
    path('view/<int:id>', views.paciente_view, name='paciente_view'),
    path('edit/<int:id>', views.paciente_edit, name='paciente_edit'),
    path('add/', views.paciente_add, name='paciente_add'),
    path('delete/<int:id>', views.paciente_delete, name='paciente_delete'),
    path('confirm_delete/<int:id>/', views.paciente_confirm_delete, name='paciente_confirm_delete'),
    path('whatsapp-redirect/<int:paciente_id>/', views.whatsapp_redirect, name='whatsapp_redirect'),
]