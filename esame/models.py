from types import NoneType

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from multiselectfield import MultiSelectField

SCELTE = [('Sat', 'Satira'),
          ('Bar', 'Barzelletta'),
          ('Bhu', 'Black Humor'),
          ('Bsq', 'Battute Squallide')]


class Battute(models.Model):
    testo = models.TextField(default="")
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    tempo = models.DateTimeField(auto_now=True)
    tipo = MultiSelectField(choices=SCELTE, max_length=3, default='bar')


    @property
    def calcolamedia(self):
        media_tupla = self.battutarec.all().aggregate(Avg('voto'))
        media_lunga=media_tupla['voto__avg']
        if type(media_lunga) is NoneType:
            media = media_lunga
        else:
            media = round(media_lunga, 2)
        return media


class Recensioni(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    battuta = models.ForeignKey(Battute, on_delete=models.CASCADE, to_field='id', related_name='battutarec')
    voto = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class ProfiloDettagliato(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    foto_profilo = models.ImageField
