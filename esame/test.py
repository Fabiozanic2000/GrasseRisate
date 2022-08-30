from django.test import TestCase, Client
from django.urls import reverse
from .models import ProfiloDettagliato
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    '''Il test fa una get per la schermata home del sito; se il codice di risposta è 200, allora questo è corretto.
    Viene inoltre controllato se il template utilizzato è quello corretto
    '''

    def test_homepage(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    '''Il seguente test cerca un profilo dettagliato con indice alto in un db vuoto, per cui sono sicuro che questa 
    non esista; per questa ragione, mi aspetto un error 404 '''

    def test_profilo_non_esistente(self):
        response = self.client.get(reverse("profilo", kwargs={'pk':800}))

        self.assertEquals(response.status_code, 404)
