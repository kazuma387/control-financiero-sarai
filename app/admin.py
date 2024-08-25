from django.contrib import admin
from .models import Paciente, Consumos, RegistroEliminado

# para administrar mejor los modelos
class PacienteAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('nombre', 'apellido', 'cedula', 'sexo', 'procedimiento')
    # para agregar un buscador
    search_fields = ('nombre', 'apellido', 'cedula', 'procedimiento')
    # para añadir filtros
    list_filter = ('sexo', 'procedimiento', 'forma_de_pago')
    # jerarquía de fechas
    date_hierarchy = 'fecha'

# para registrar el modelo y salga en el panel de admin
admin.site.register(Paciente, PacienteAdmin)


# para administrar mejor los modelos
class ConsumosAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('producto', 'costo', 'fecha')
    # para agregar un buscador
    search_fields = ('producto', 'costo', 'fecha')
    # para añadir filtros
    list_filter = ('producto', 'costo', 'fecha')
    # jerarquía de fechas
    date_hierarchy = 'fecha'

admin.site.register(Consumos, ConsumosAdmin)


# para administrar mejor los modelos
class RegistroEliminadoAdmin(admin.ModelAdmin):
    # para que salga todo esto en el panel
    list_display = ('tipo', 'datos', 'eliminado_por', 'fecha_eliminacion')
    # para agregar un buscador
    search_fields = ('tipo', 'eliminado_por', 'fecha_eliminacion')
    # para añadir filtros
    list_filter = ('tipo', 'eliminado_por', 'fecha_eliminacion')
    # jerarquía de fechas
    date_hierarchy = 'fecha_eliminacion'

admin.site.register(RegistroEliminado, RegistroEliminadoAdmin)
