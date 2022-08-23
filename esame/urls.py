"""esame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from esame import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrazioneView.as_view(), name='registrazione'),
    path('add', views.AggiungiBattuta.as_view(), name='aggiungi_battuta'),
    path('profile/<int:pk>', views.ProfiloView.as_view(), name='profilo'),
    path('review/<int:pk>', views.AggiungiRecensione.as_view(), name='aggiungi_recensione'),
    path('modify/<int:pk>', views.ModificaProfilo.as_view(), name='modifica_profilo'),
    path('filter/', views.filtro, name='filtro'),
    path('filtered/<str:tipo>', views.VistaFiltrata.as_view(), name='vista_filtrata'),
    path('follow/<int:pk>', views.FollowView.as_view(), name='follow'),
    path('/feed', views.FeedView.as_view(), name='feed')
]
