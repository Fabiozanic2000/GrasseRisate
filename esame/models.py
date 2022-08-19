from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
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


class Recensioni(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    battuta = models.ForeignKey(Battute, on_delete=models.CASCADE)
    voto = models.SmallIntegerField(validators=[MinValueValidator('1'), MaxValueValidator('10')])
