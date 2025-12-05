from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    name = models.CharField(max_length=30, verbose_name='Cômodo')

    def __str__(self) -> str:
        return self.name
    
class Device(models.Model):
    device_id = models.IntegerField(
        primary_key=True,
        verbose_name='ID do dispositivo'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Cômodo",
        null=True
    )

    name = models.CharField(
        max_length=50,
        verbose_name='Nome do dispositivo'
    )

    port = models.SmallIntegerField(
        verbose_name='Porta'
    )

    device_type = models.BooleanField(
        verbose_name='Atuador(0)|Sensor(1)',
        default=False
    )

    device_input = models.BooleanField(
        verbose_name='Analogico(0)|Digital(1)',
        default=False
    )

    analog_value = models.PositiveSmallIntegerField(
        verbose_name='Valor analógico (0-255)',
        default=0
    )

    digital_value = models.BooleanField(
        verbose_name='Valor digital',
        default=False
    )

    def __str__(self):
        return f"{self.name} (ID: {self.device_id})"
