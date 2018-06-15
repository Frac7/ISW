# -*- coding: utf-8 -*-
from __future__ import unicode_literals #per lettere accentate...
from django.contrib.auth.decorators import login_required
from GestioneHotel.models import *
from django.shortcuts import render

# Create your views here.
#Hotel: viste legate alla classe Hotel
@login_required(login_url='/Login.html') #è da provare
def listaCamere(request, hotelID):
    #Controlla prima che l'hotel con id hotelID esista
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    #Date tutte le camere registrare nel db, prende quelle presenti in hotel
    lista = []
    for camera in Camera.objects.all():
        if camera.hotel.__eq__(hotel):
            lista.append(camera)
    #Qui ci sono ancora le pagine html statiche da rendere dinamiche
    return render(request,
                  "InfoHotelAggiungiCamera.html", {
                      'camere': lista #lista delle camere da scorrere in html
                  })
@login_required(login_url='/Login.html') #è da provare
def dettagliHotel(request, hotelID):
    #Controlla prima che l'hotel con id hotelID esista
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    #Dato un id, si restituisce l'hotel corrispondente
    return render(request,
                  "InfoHotelAggiungiCamera.html", {
                      'hotel': hotel #lista delle camere da scorrere in html
                  })
#Albergatore
def autorizzaAccesso(request, email, password):
    pass
def listaHotel(request, albergatoreID):
    try:
        albergatore = Albergatore.objects.get(id=albergatoreID)
    except Albergatore.DoesNotExist:
        albergatore = None
        listaHotel = []
        for hotel in Hotel.objects.all():
            if hotel.proprietario.__eq__(albergatore):
                listaHotel.append(hotel)
        return render(request,
                      "AggiungiHotel_provaDinamica.html",{
                        'listaHotel' : listaHotel
                      })

    pass
def prenotazionePerAlbergatore(request, albergatoreID):
    pass
#Camera
def disponibilita(request, cameraID, dal, al):
    pass
