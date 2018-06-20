# -*- coding: utf-8 -*-
from __future__ import unicode_literals #Per lettere accentate...
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from GestioneHotel.models import *
from GestioneHotel.forms import *
from django.shortcuts import render
from django.utils import timezone
import datetime

# Create your views here.
#Hotel: viste legate alla classe Hotel
@login_required(login_url='/Login') #è da provare
#dettagli hotel e lista camere
def dettaglioHotel(request, hotelID):
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    #Date tutte le camere registrare nel db, prende quelle presenti in hotel
    if hotel != None:
        # Collegato al form aggiungi camera
        if request.method == "POST":  # Useremo sempre la post per i form
            aggiungiCameraForm = AggiungiCameraForm(request.POST)
            # Recupera il form e controlla che sia valido, se sì crea una camera
            if aggiungiCameraForm.is_valid():
                listaServizi = []
                if aggiungiCameraForm.cleaned_data['servizio1'] == True:
                    listaServizi.append(Servizio.objects.all().get(nome="TV"))
                if aggiungiCameraForm.cleaned_data['servizio2'] == True:
                    listaServizi.append(Servizio.objects.all().get(nome="AC"))
                if aggiungiCameraForm.cleaned_data['servizio3'] == True:
                    listaServizi.append(Servizio.objects.all().get(nome="FB"))
                #Servizi esistenti recuperati da checkbox
                nuovaCamera = Camera(id=(len(Camera.objects.all())+1),numero=aggiungiCameraForm.cleaned_data['numero'],
                                     postiLetto=aggiungiCameraForm.cleaned_data['postiLetto'],
                                     hotel=hotel)
                nuovaCamera.save()
                for servizio in listaServizi:
                    nuovoServizioDisponibile = ServiziDisponibili(camera=nuovaCamera, servizio=servizio)
                    nuovoServizioDisponibile.save()
                # Salvataggio camera nel db
        lista = hotel.listaCamere()
        servizi = {} #Dizionario: key = id camera, value = servizio (ottenuto filtrando prima i servizi per camera e poi i servizi per id)
        for camera in lista:
            servizi[camera.id] = camera.listaServizi()
        aggiungiCameraForm = AggiungiCameraForm()
    else:
        lista = []
        servizi = {}
        aggiungiCameraForm = None
    #Qui ci sono ancora le pagine html statiche da rendere dinamiche
    return render(request, "InfoHotelAggiungiCamera.html", {
                      "hotel": hotel,
                      "camere": lista, #lista delle camere da scorrere in html
                        "servizi": servizi,
        "form": aggiungiCameraForm
                  })
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


def aggiungiHotel(request, albergatoreID):
    try:
        albergatore=Albergatore.objects.get(id=albergatoreID)
    except Albergatore.DoesNotExist:
        albergatore=None
    if request.method=="POST":
        aggiungiHotelForm=AggiungiHotelForm(request.POST)
        if aggiungiHotelForm.is_valid():
            nuovoIndirizzo=Indirizzo(via=aggiungiHotelForm.cleaned_data['via'],
                                     numero=aggiungiHotelForm.cleaned_data['numero'])
            nuovoIndirizzo.save()

            nuovoHotel=Hotel(nome=aggiungiHotelForm.cleaned_data['nome'],
                             descrizione=aggiungiHotelForm.cleaned_data['descrizione'],
                             citta=aggiungiHotelForm.cleaned_data['citta'],
                             indirizzo=nuovoIndirizzo,
                             proprietario=albergatore)
            nuovoHotel.save()
    return HttpResponseRedirect("AggiungiHotel/" + albergatoreID + "/")

def listaHotel(request, albergatoreID):
    try:
        albergatore = Albergatore.objects.get(id=albergatoreID)
    except Albergatore.DoesNotExist:
        albergatore = None

    listaHotel = [[],[]]

    for hotel in Hotel.objects.all():
        if hotel.proprietario.__eq__(albergatore):
            listaHotel.append(hotel)
            listaHotel.append(hotel.contaCamere())

    return render(request,
                    "AggiungiHotel.html",{
                    'listaHotel' : listaHotel,
                    'form':AggiungiHotelForm
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
                    "Home.html",{
                    'listaPrenotazioni':listaPrenotazioni
                    })

#Camera
def disponibilita(request, cameraID, dal, al):
    pass

def Main(request):
    if request.method == "POST":
        # Da Main se clic su cerca...
        formRicerca = FormRicerca(request.POST)
        #se il form è correttamente compilato...
        if formRicerca.is_valid():
            citta=formRicerca.cleaned_data['citta']
            dataArrivo=formRicerca.cleaned_data['dataArrivo']
            dataPartenza = formRicerca.cleaned_data['dataPartenza']
            posti = formRicerca.cleaned_data['posti']
            # recupero le camere libere
            camere=(Camera.objects.exclude(id__in=Prenotazione.objects.filter(checkin__lte=dataArrivo,checkout__gt=dataArrivo\
                    )).exclude(id__in=Prenotazione.objects.filter(checkin__lt=dataPartenza,checkout__gte=dataPartenza\
                    )).exclude(id__in=Prenotazione.objects.filter(checkin__gte=dataArrivo, checkout__lte=dataPartenza))).filter(postiLetto=posti).filter(hotel=Hotel.objects.filter(citta=citta))

            if len(camere)==0:
                # se nessuna Camera è stata trovata...
                noresult=True
                # riporta a Main.html con un flag per la visualizzazione di un messaggio
                return render(request, "Main.html", {'form': formRicerca,'noresult':noresult})
            else:
                # se almeno una camera è stata trovata
                servizi=Servizio.objects.all()
                serviziDisponibili=ServiziDisponibili.objects.all()
                return render(request,"ListaCamereDisponibili.html",{'camere':camere,'serviziDisponibili':serviziDisponibili,'servizi':servizi,'dataArrivo':dataArrivo,'dataPartenza':dataPartenza})
    else:
        return render(request, "Main.html", {'form': FormRicerca})

def ListaCamereDisponibili(request):
    return render(request, "ListaCamereDisponibili.html")

def Prenota(request,nomeHotel,numeroCamera,postiLetto,idCamera,arrivo,partenza):
    if request.method == "POST":
        # Registare la prenotazione
        formPrenota = FormPrenota(request.POST)
        if formPrenota.is_valid():
            #recupero i dati della prenotazione
            nuovaPrenotazione=Prenotazione()
            utente = formPrenota.cleaned_data['prenotaUtente']
            arrivo = formPrenota.cleaned_data['prenotaCheckin']
            partenza = formPrenota.cleaned_data['prenotaCheckout']
            idCamera = formPrenota.cleaned_data['prenotaIdCamera']
            # Qui il slvataggio
            nuovaPrenotazione.utente=utente
            nuovaPrenotazione.checkin=datetime.datetime.strptime(arrivo, "%d-%m-%Y")
            nuovaPrenotazione.checkout=datetime.datetime.strptime(partenza, "%d-%m-%Y")
            nuovaPrenotazione.camera=Camera.objects.get(id=idCamera)
            nuovaPrenotazione.save()

            return render(request, "PrenotazioneEffettuata.html")
        else:
            return render(request, "Main.html")
    else:
        #imposto i valori di default nella form (sono campi hidden
        formPrenota = FormPrenota(initial={'prenotaCheckout': partenza,'prenotaCheckin': arrivo, 'prenotaIdCamera': idCamera})

        return render(request, "Prenota.html", {'form':formPrenota,'nomeHotel':nomeHotel,'numeroCamera':numeroCamera,'postiLetto':postiLetto,'idCamera':idCamera,'arrivo':arrivo,'partenza':partenza})


def PrenotazioneEffettuata(request):
    return render(request, "PrenotazioneEffettuata.html")