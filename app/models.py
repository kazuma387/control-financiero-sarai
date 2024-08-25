from django.db import models
from django.contrib.auth.models import User

# creando DB de pacientes
class Paciente(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False, null=False)
    cedula = models.CharField(max_length=10, blank=False, null=False)
    sexo = models.CharField(max_length=10, blank=False, null=False)
    telefono = models.CharField(max_length=12, default='57', blank=True, null=True)
    procedimiento = models.CharField(max_length=100, blank=False, null=False)
    observaciones = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    forma_de_pago = models.CharField(max_length=50, blank=False, null=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - C.I: {self.cedula}"
    
# creando DB de consumos y gastos
class Consumos(models.Model):
    producto = models.CharField(max_length=100, blank=False, null=False)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} {self.costo}"

# creando DB de eliminados
class RegistroEliminado(models.Model):
    tipo = models.CharField(max_length=20)  # 'paciente' o 'consumos y gastos'
    datos = models.JSONField()
    eliminado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_eliminacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} eliminado el {self.fecha_eliminacion}"