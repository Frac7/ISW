# -*- coding: utf-8 -*-
from __future__ import unicode_literals #Per lettere accentate...
from django.contrib.auth.decorators import login_required
from GestioneHotel.models import *
from GestioneHotel.forms import *
from django.shortcuts import render

# Create your views here.
#Hotel: viste legate alla classe Hotel
@login_required(login_url='/Login.html') #è da provare
#dettagli hotel e lista camere
def listaCamere(request, hotelID):
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    #Date tutte le camere registrare nel db, prende quelle presenti in hotel
    if hotel != None:
        lista = Camera.objects.filter(hotel=hotel)
    else:
        lista = []
    #Qui ci sono ancora le pagine html statiche da rendere dinamiche
    return render(request,
                  "InfoHotelAggiungiCamera.html", {
                      "hotel": hotel,
                      "camere": lista #lista delle camere da scorrere in html
                  })
#Collegato al form aggiungi camera
@login_required(login_url='/Login.html') #è da provare
def aggiungiCamera(request, hotelID):
    #Cliccando su un hotel non si dovrebbe avere questo problema, ma non si sa mai
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    if request.method == "POST": #Useremo sempre la post per i form
        #Per i click su camera o hotel si può usare la get in modo da recuperare i parametri e poter usare query strings
        aggiungiCameraForm = AggiungiCameraForm(request.POST)
        #Recupera il form e controlla che sia valido, se sì crea una camera
        if aggiungiCameraForm.is_valid():
            nuovaCamera = Camera(numero=aggiungiCameraForm.cleaned_data['numeroCamera'],
                           postiLetto=aggiungiCameraForm.cleaned_data['postiLettoCamera'],
                                 hotel=hotel)
            #TODO: associazione id camera e servizi (n a m)
            nuovaCamera.save()
            #Salvataggio camera nel db
    return render(request,
                "InfoHotelAggiungiCamera.html?hotelID = " + hotelID + "/",)
    #Per ora viene restituita la stessa pagina in tutti i casi

#Albergatore
def aggiungiAlbergatore(request):
    if request.method== "POST":
        registrazioneAlbergatore= RegistrazioneAlbergatore(request.POST)
        if registrazioneAlbergatore.is_valid():
            nuovoAlbergatore= Albergatore(nome=registrazioneAlbergatore.cleaned_data['nome'],
                                          cognome=registrazioneAlbergatore.cleaned_data['cognome'],
                                          email=registrazioneAlbergatore.cleaned_data['email'],
                                          password=registrazioneAlbergatore.cleaned_data['password'])
            nuovoAlbergatore.save()
            return HttpResponse("Albergatore salvato")#what? copiato senza sapere cosa SIA
        else:
            registrazioneAlbergatore=RegistrazioneAlbergatore()
    return render(request, "Registrazione.html", {"form" : registrazioneAlbergatore})

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

def prenotazionePerAlbergatore(request, albergatoreID):
    try:
        albergatore=Albergatore.objects.get(id=albergatoreID)
    except Albergatore.DoesNotExist:
        albergatore= None
        listaPrenotazioni = []
        for prenotazione in Prenotazione.objects.all():
            if prenotazione.camera.hotel.proprietario.__eq__(albergatore):
                listaPrenotazioni.append(prenotazione)
        return render(request,
                      "Home_provaDinamica.html",{
                        'listaPrenotazioni':listaPrenotazioni
                      })

#Camera
def disponibilita(request, cameraID, dal, al):
    pass
