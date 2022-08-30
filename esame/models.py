from types import NoneType

from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, signals

SCELTE = [('Satira', 'Satira'),
          ('Barzelletta', 'Barzelletta'),
          ('Black humor', 'Black Humor'),
          ('Battuta squallida', 'Battuta Squallida'),
          ('Gioco di parole', 'Gioco di parole'),
          ('Notizia divertente', 'Notizia divertente')]


class Battute(models.Model):
    testo = models.TextField(default="")
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='utentebat')
    tempo = models.DateTimeField(auto_now=True)
    tipo = models.CharField(choices=SCELTE, default='bar', max_length=25)

    def __str__(self):
        return self.testo + " " + self.tipo

    @property
    def calcola_media(self):
        media_tupla = self.battutarec.all().aggregate(Avg('voto'))
        media_lunga = media_tupla['voto__avg']
        if type(media_lunga) is NoneType:
            media = media_lunga
        else:
            media = round(media_lunga, 2)
        return media


class Recensioni(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    battuta = models.ForeignKey(Battute, on_delete=models.CASCADE, to_field='id', related_name='battutarec')
    voto = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Followers(models.Model):
    seguitore = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utente_seguitore")
    seguito = models.ForeignKey(User, on_delete=models.CASCADE, related_name="utente_seguito")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seguitore', 'seguito'], name='relazione di follow')
        ]


class ProfiloDettagliato(models.Model):
    utente = AutoOneToOneField(User, on_delete=models.CASCADE, related_name='ciao', primary_key=True)
    foto_profilo = models.ImageField(null=True, blank=True, upload_to='images/')
    bio = models.TextField(default="", blank=True)
    nome = models.CharField(max_length=25, blank=True)
    cognome = models.CharField(max_length=50, blank=True)
    datadinascita = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    citta = models.CharField(max_length=50, blank=True)

    @property
    def media_profilo(self):
        qs = Battute.objects.filter(utente=self.utente)
        qs2 = Recensioni.objects.filter(battuta__in=qs).aggregate(Avg('voto')).get('voto__avg')
        if type(qs2) is NoneType:
            media = qs2
        else:
            media = round(qs2, 2)
        return media


def create_model_b(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        ProfiloDettagliato.objects.create(utente=instance)


signals.post_save.connect(create_model_b, sender=User, weak=False,
                          dispatch_uid='models.create_model_b')
