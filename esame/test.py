from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Battute


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    """
    Il test fa una get per la schermata home del sito; se il codice di risposta è 200, allora questo è corretto.
    Viene inoltre controllato se il template utilizzato è quello corretto
    """

    def test_homepage(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    """
    Il seguente test cerca un profilo dettagliato con indice alto in un db vuoto, per cui sono sicuro che questa 
    non esista; per questa ragione, mi aspetto un error 404 
    """

    def test_profilo_non_esistente(self):
        response = self.client.get(reverse("profilo", kwargs={'pk': 800}))

        self.assertEquals(response.status_code, 404)


class TestModel(TestCase):
    """
    Il test crea un nuovo utente con una battuta, e controlla come questa viene salvata utilizzando il metodo __str__
    del modello
    """

    def test_nuova_battuta(self):
        utente = User.objects.create_user(username="prova")
        utente.set_password("aabbaabb")
        utente.save()

        battuta = Battute.objects.create(utente=utente,
                                         testo="Battuta divertente",
                                         tipo="Satira")

        battuta.save()

        self.assertEqual(str(battuta), "Battuta divertente Satira")
