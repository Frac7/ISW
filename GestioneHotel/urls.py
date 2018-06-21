"""GestioneHotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from GestioneHotel import views

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Home/(?P<albergatoreID>\d+)/', views.prenotazionePerAlbergatore),
    url(r'InfoHotelAggiungiCamera/(?P<hotelID>\d+)/', views.dettaglioHotel, name='hotelID'),
    url(r'AggiungiHotel/(?P<albergatoreID>\d+)/', views.listaHotel, name ='albergatoreID'),
    #url(r'^Main/', views.Main), #questa sara' la pagina iniziale, quindi si dovrebbe inserire $ al posto di Main/
    url(r'^$', views.Main), #questa sara' la pagina iniziale, quindi si dovrebbe inserire $ al posto di Main/
    url(r'^ListaCamereDisponibili/', views.ListaCamereDisponibili),
    url(r'^Prenota/(?P<nomeHotel>\D+)/(?P<numeroCamera>[\w-]+)/(?P<postiLetto>\d+)/(?P<idCamera>\d+)/(?P<arrivo>[\w-]+)/(?P<partenza>[\w-]+)/', views.Prenota),
    url(r'PrenotazioneEffettuata/', views.PrenotazioneEffettuata),
    url(r'^signup/', views.signup),
    url(r'^Login/', views.signin),
    url(r'Logout/', views.signout),
]

