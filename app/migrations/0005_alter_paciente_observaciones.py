# Generated by Django 5.1 on 2024-08-22 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_paciente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
