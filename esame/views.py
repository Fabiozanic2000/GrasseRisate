from types import NoneType

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView

from esame.forms import FormFiltro, FormRicercaProfilo
from esame.models import Battute, Recensioni, ProfiloDettagliato, Followers


class HomeView(ListView):
    template_name = 'home.html'
    model = Battute

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.order_by('-tempo').exclude(utente_id=self.request.user.id)
        else:
            return self.model.objects.order_by('-tempo')


class RegistrazioneView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registrazione.html'
    success_url = reverse_lazy('home')


class AggiungiBattuta(LoginRequiredMixin, CreateView):
    model = Battute
    template_name = 'aggiunta_battuta.html'
    fields = ('testo', 'tipo')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.utente = self.request.user
        return super().form_valid(form)


class ProfiloView(DetailView):
    template_name = 'profilo.html'
    model = ProfiloDettagliato

    def get_context_data(self, **kwargs):

        context = super(ProfiloView, self).get_context_data(**kwargs)
        context['nomeutente'] = User.objects.filter(id=self.kwargs['pk']).get().username

        qs = Battute.objects.filter(utente=self.kwargs['pk'])
        qs2 = Recensioni.objects.filter(battuta__in=qs).aggregate(Avg('voto')).get('voto__avg')
        if type(qs2) is NoneType:
            media_arrotondata = qs2
        else:
            media_arrotondata = round(qs2, 2)
        context['media'] = media_arrotondata
        context['followers'] = Followers.objects.filter(seguito=self.kwargs['pk']).count()
        context['following'] = Followers.objects.filter(seguitore=self.kwargs['pk']).count()
        if self.request.user.is_authenticated:
            puo_seguire = Followers.objects.filter(seguitore=self.request.user, seguito_id=self.kwargs['pk'])
            if puo_seguire:
                context['puo_seguire'] = False
            else:
                context['puo_seguire'] = True
        else:
            context['puo_seguire'] = False

        return context


class AggiungiRecensione(LoginRequiredMixin, CreateView):
    model = Recensioni
    template_name = 'aggiungi_recensione.html'
    fields = ('voto',)
    success_url = reverse_lazy('home')

    def form_valid(self, form, ):
        form.instance.utente = self.request.user
        form.instance.battuta_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AggiungiRecensione, self).get_context_data(**kwargs)
        conteggio = Recensioni.objects.filter(battuta=self.kwargs['pk'], utente=self.request.user).count()
        utente_battuta = Battute.objects.get(id=self.kwargs['pk'])
        if utente_battuta.utente_id == self.request.user.id:
            context['autorecensione'] = True
        else:
            context['autorecensione'] = False

        if conteggio >= 1:
            context['puo_recensire'] = False
        else:
            context['puo_recensire'] = True
        return context


class ModificaProfilo(LoginRequiredMixin, UpdateView):
    model = ProfiloDettagliato
    template_name = 'modifica_profilo.html'
    fields = ('nome', 'cognome', 'foto_profilo', 'datadinascita', 'email', 'citta', 'bio')
    success_url = reverse_lazy('home')


def filtro(request):
    if request.method == "POST":
        form = FormFiltro(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data.get('tipo')
            return redirect("vista_filtrata", tipo)

    else:
        form = FormFiltro()

    return render(request, template_name='form_filtro.html', context={"form": form})


class VistaFiltrata(ListView):
    template_name = 'vista_filtrata.html'
    model = Battute

    def get_queryset(self):
        tipo2 = self.request.resolver_match.kwargs['tipo']
        qs = Battute.objects.filter(tipo=tipo2).order_by('-tempo')
        return qs


class FollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Followers(seguitore=request.user, seguito_id=self.kwargs['pk']).save()
        url = reverse("profilo", kwargs={"pk": self.kwargs['pk']})
        return HttpResponseRedirect(url)


class FeedView(LoginRequiredMixin, ListView):
    model = Battute
    template_name = 'feed.html'

    def get_queryset(self):
        qs = Followers.objects.filter(seguitore=self.request.user).values('seguito')
        qs2 = Battute.objects.filter(utente__in=qs).order_by('-tempo')
        return qs2

    def get_context_data(self, **kwargs):
        context = super(FeedView, self).get_context_data(**kwargs)
        lista = [(persona.media_profilo, persona.utente) for persona in ProfiloDettagliato.objects.all() if
                 type(persona.media_profilo) is not NoneType]
        lista.sort(reverse=True, key=lambda x: x[0])
        context['quanti'] = len(lista)
        if len(lista) >= 1:
            context['primo'] = lista[0][1]
            context['primamedia'] = lista[0][0]
        if len(lista) >= 2:
            context['secondo'] = lista[1][1]
            context['secondamedia'] = lista[1][0]
        if len(lista) >= 3:
            context['terzo'] = lista[2][1]
            context['terzamedia'] = lista[2][0]
        chi_segue = Followers.objects.filter(seguitore=self.request.user.id).values_list('seguito_id')
        id_altri = User.objects.exclude(id__in=chi_segue).exclude(id=self.request.user.id).values_list('id')
        id_altri_det = ProfiloDettagliato.objects.filter(utente_id__in=id_altri)
        lista = [(persona.media_profilo, persona.utente) for persona in id_altri_det if
                 type(persona.media_profilo) is not NoneType]
        lista.sort(reverse=True, key=lambda x: x[0])
        if len(lista) > 0:
            context['test'] = True
            context['migliore_following'] = lista[0][1]
            context['migliore_media'] = lista[0][0]
        else:
            context['test'] = False
        return context


def cerca_profilo(request):
    if request.method == "POST":
        form = FormRicercaProfilo(request.POST)
        if form.is_valid():
            nick = form.cleaned_data.get('nick')
            test = User.objects.filter(username=nick).count()
            if test >= 1:
                nick_id = User.objects.filter(username=nick).get().id
                return redirect("profilo", nick_id)
            else:
                return redirect("errore_ricerca")

    else:
        form = FormRicercaProfilo()

    return render(request, template_name='form_ricerca.html', context={"form": form})


class ErroreRicerca(TemplateView):
    template_name = "errore_ricerca.html"


class BattuteProfilo(ListView):
    template_name = "battute_profilo.html"
    model = Battute

    def get_queryset(self):
        qs = Battute.objects.filter(utente_id=self.kwargs['pk']).order_by('-tempo')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BattuteProfilo, self).get_context_data(**kwargs)
        context['nickname'] = User.objects.filter(id=self.kwargs['pk']).get().username
        if self.request.user.id == self.kwargs['pk']:
            context['puo_recensire'] = False
        else:
            context['puo_recensire'] = True
        return context
