from django.urls import path, include

urlpatterns = [
    path('paciente/', include('app.paciente_urls')),
    path('consumos/', include('app.consumos_urls')),
    path('totales/', include('app.totales_urls')),
]