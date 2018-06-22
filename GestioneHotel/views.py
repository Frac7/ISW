# -*- coding: utf-8 -*-
from __future__ import unicode_literals #Per lettere accentate...
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden

from GestioneHotel.forms import *
import datetime
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


def signup(request):
    # Se risulta un utente gia' loggato nella sessione
    if request.user.is_authenticated:
        id = Albergatore.objects.all().get(email=request.user).id
        return redirect("/Home/" + str(id))  # L'utente loggato che cerca di registrarsi viene rimandato alla sua home (deve prima fare logout)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            nome = form.cleaned_data.get('nome')
            cognome = form.cleaned_data.get('cognome')
            raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            # Una volta Registrato dovrebbe fare un login automatico
            #login(request, user)
            # Bisogna anche creare l'Albergatore
            albergatore=Albergatore(nome=nome, cognome=cognome, email=username, password=raw_password)
            albergatore.save()

            # Se viene attivato il login automatico si deve fare il redirect alla sua home
            #return redirect('/Home/'+str(albergatore.id))
            # Altrimenti redirect a Main
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


#Logout
@login_required(login_url='/Login') #Per effettuare il logout è richiesto il login
def signout(request): #View logout
    #Distrugge la sessione
    logout(request)
    #Si ritorna al main, la pagina del sito che vedono gli utenti non registrati
    return redirect("/")

#Login
def signin(request):
    #Se risulta un utente gia' loggato nella sessione
    if request.user.is_authenticated:
        #Inizializzazione variabile id
        id = Albergatore.objects.all().get(email=request.user).id
        return redirect("/Home/" + str(id)) #L'utente loggato che cerca di accedere viene rimandato alla sua home
    error = False #Inizializzazione variabile per i messaggi di errore
    if request.method == "POST":  # Se il metodo della richiesta è POST
        loginForm = LoginForm(request.POST) #Si recuperano le informazioni del login form
        #Se il form è valido (le informazioni inserite nel form)
        if loginForm.is_valid():
            #Si recupera il testo dal campo email
            email = loginForm.cleaned_data['email']
            #Si recupera il testo dal campo password
            password = loginForm.cleaned_data['password']
            # Autenticazione: chi è l'utente
            user = authenticate(username=email, password=password)
            #Se l'utente esiste
            if user != None:
                id = Albergatore.objects.all().get(email=user).id
                #Login utente
                login(request, user)
                #L'utente viene mandato nella sua home
                return redirect("/Home/" + str(id))
            else:
                #Errore: l'utente non esiste
                error = True
        #Errore: form non valido
        else:
            error = True
    #Nuovo form vuoto nel caso in cui non sia stata presentata una richiesta POST, es: primo caricamento della pagina senza inserimento dati
    loginForm = LoginForm()
    #Restituzione template e campi dinamici
    return render(request, "Login.html", {
        "form": loginForm,
        "error": error
    })

#Hotel
@login_required(login_url='/Login') #Questa pagina è visibile solo da un albergatore, utente registrato
#Dettagli hotel e lista camere, viene passato con POST l'id dell'hotel interessato
def dettaglioHotel(request, hotelID):
    #Inizializzazione variabile per indicare l'assenza di camere nell'hotel (nessuna camera ancora aggiunta)
    nessunCamera = False
    #Recupera l'hotel in base all'ID
    try:
        hotel = Hotel.objects.get(id=hotelID)
    except Hotel.DoesNotExist:
        hotel = None
    #Date tutte le camere registrare nel db, prende quelle presenti in hotel
    if hotel != None: #Se l'hotel esiste
        email = Hotel.objects.all().get(id=hotelID).proprietario.email
        # Tentativo di accesso ad una pagina di un altro albergatore tramite hotel id diverso (da uno di quelli possibili, quindi posseduti) in barra indirizzi
        if not (str(request.user).__eq__(str(email))):
            id = Albergatore.objects.all().get(email=request.user).id
            return redirect("/Home/" + str(id)) #Utente rimandato alla sua home
            #return HttpResponseForbidden() # Variante con codice 403
        # Collegato al form aggiungi camera
        if request.method == "POST":  #In caso di richiesta POST
            aggiungiCameraForm = AggiungiCameraForm(request.POST)
            # Recupera il form e controlla che sia valido, se sì crea una camera
            if aggiungiCameraForm.is_valid():
                listaServizi = [] #Vengono aggiunti i servizi in base a quelli disponibili
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
                # Salvataggio camera nel DB
                for servizio in listaServizi:
                    nuovoServizioDisponibile = ServiziDisponibili(camera=nuovaCamera, servizio=servizio)
                    nuovoServizioDisponibile.save()
                #Salvataggio della coppia camera/servizio nel DB
        #Recuperare la lista delle camere per l'hotel
        lista = hotel.listaCamere()
        servizi = {} #Dizionario: key = id camera, value = servizio (ottenuto filtrando prima i servizi per camera e poi i servizi per id)
        for camera in lista:
            servizi[camera.id] = camera.listaServizi()
        #Form vuoto per aggiungere una camera all'hotel
        aggiungiCameraForm = AggiungiCameraForm()
        #Viene stampato un messaggio apposito nella pagina se ancora nessuna camera è stata aggiunta all'hotel
        if len(lista) == 0:
            nessunCamera = True
    else:
        #Se l'hotel non è stato trovato, la risposta avrà codice 404 (not found)
        return HttpResponseNotFound()
    #Viene mostrata la pagina del dettaglio hotel con tutte le informazioni dinamiche
    return render(request, "InfoHotelAggiungiCamera.html", {
                    "albergatoreID" : hotel.proprietario.id,
                      "hotel": hotel,
                      "camere": lista, #lista delle camere da scorrere in html
                        "servizi": servizi,
                    "vuoto": nessunCamera,
        "form": aggiungiCameraForm
                  })
#Albergatore
@login_required(login_url='/Login')
def listaHotel(request, albergatoreID):
    nessunHotel = False
    try:
        albergatore = Albergatore.objects.all().get(id=albergatoreID) #Si recupera l'albergatore da albergatore id
        # Tentativo di accesso ad una pagina di un altro albergatore tramite albergatore id
        if not (str(request.user).__eq__(str(albergatore.email))): #Se l'albergatore a cui corrisponde albergatore id è diverso dall'utente loggato
            id = Albergatore.objects.all().get(email=request.user).id
            return redirect("/AggiungiHotel/" + str(id)) #L'utente viene rimandato alla sua pagina aggiungi hotel
    except Albergatore.DoesNotExist:
        albergatore = None
    if albergatore != None:
        if request.method == "POST":
            aggiungiHotelForm = AggiungiHotelForm(request.POST)

            if aggiungiHotelForm.is_valid():
                nuovoIndirizzo = Indirizzo(via=aggiungiHotelForm.cleaned_data['via'],
                                           numero=aggiungiHotelForm.cleaned_data['numeroCivico'])
                nuovoIndirizzo.save()

                nuovoHotel = Hotel(nome=aggiungiHotelForm.cleaned_data['nome'],
                                   descrizione=aggiungiHotelForm.cleaned_data['descrizione'],
                                   citta=aggiungiHotelForm.cleaned_data['citta'],
                                   indirizzo=nuovoIndirizzo,
                                   proprietario=albergatore)
                nuovoHotel.save()

        aggiungiHotelForm= AggiungiHotelForm()
        listaHotel= []
        for hotel in Hotel.objects.all():
            if hotel.proprietario.__eq__(albergatore):
                listaHotel.append(hotel)
                listaHotel.append(len(hotel.listaCamere()))
        if len(listaHotel) == 0:
            nessunHotel = True
    else:
        return HttpResponseNotFound() #Albergatore non esistente, risposta 404
    return render(request,
                    "AggiungiHotel.html",{
                    'albergatoreID' : albergatore.id,
                    'listaHotel' : listaHotel,
                    'form':aggiungiHotelForm,
                    'vuoto': nessunHotel
                    })

@login_required(login_url='/Login')
def prenotazionePerAlbergatore(request, albergatoreID):
    nessunaPrenotazione = False
    try:
        albergatore = Albergatore.objects.all().get(id=albergatoreID)  # Si recupera l'albergatore da albergatore id
        # Tentativo di accesso ad una pagina di un altro albergatore tramite albergatore id
        if not (str(request.user).__eq__(str(
                albergatore.email))):  # Se l'albergatore a cui corrisponde albergatore id è diverso dall'utente loggato
            id = Albergatore.objects.all().get(email=request.user).id
            return redirect("/Home/" + str(id)) #L'utente viene rimandato alla sua pagina prenotazioni
    except Albergatore.DoesNotExist:
        albergatore= None
    if albergatore != None:
        listaPrenotazioni = []
        for prenotazione in Prenotazione.objects.all():
            if prenotazione.camera.hotel.proprietario.__eq__(albergatore):
                listaPrenotazioni.append(prenotazione)
        if len(listaPrenotazioni) == 0:
            nessunaPrenotazione = True
    else:
        return HttpResponseNotFound() #Albergatore non trovato, errore 404
    return render(request,
                    "Home.html",{
            'albergatoreID': albergatoreID,
                    'listaPrenotazioni':listaPrenotazioni,
                    'vuoto': nessunaPrenotazione
                    })

def Main(request):

    if request.user.is_authenticated: #Se l'utente ha fatto login
        id = Albergatore.objects.all().get(email=request.user).id  # Si recupera l'id albergatore con l'email
        return redirect("/Home/"+str(id)) #Viene rimandato alla sua home (in teoria non sono previste prenotazioni per gli utenti loggati)
    if request.method == "POST":
        # Da Main se clic su cerca...
        formRicerca = FormRicerca(request.POST)

        #se il form è correttamente compilato...
        if formRicerca.is_valid():
            citta=formRicerca.cleaned_data['citta']
            dataArrivo=formRicerca.cleaned_data['dataArrivo']
            dataPartenza = formRicerca.cleaned_data['dataPartenza']
            posti = formRicerca.cleaned_data['posti']


            # Controllo che le date non siano precedenti alla data di oggi
            if dataArrivo < datetime.date.today() or dataArrivo < datetime.date.today():
                msg="Attenzione: le date di arrivo e di partenza non possono essere precedenti ad oggi"
                return render(request, "Main.html", {'form': formRicerca, 'msg': msg})

            # Controllo che la data di partenza sia successiva a quella di arrivo
            if dataArrivo >= dataPartenza:
                msg="Attenzione: la data di partenza deve essere successiva a quella di arrivo"
                return render(request, "Main.html", {'form': formRicerca, 'msg': msg})

            # recupero le camere libere
            camerelibere=(Camera.objects.exclude(id__in=Prenotazione.objects.filter(checkin__lte=dataArrivo,checkout__gt=dataArrivo\
                    )).exclude(id__in=Prenotazione.objects.filter(checkin__lt=dataPartenza,checkout__gte=dataPartenza\
                    )).exclude(id__in=Prenotazione.objects.filter(checkin__gte=dataArrivo, checkout__lte=dataPartenza))).filter(postiLetto=posti).filter(hotel__in=Hotel.objects.filter(citta=citta))

            if len(camerelibere)==0:
                # se nessuna Camera è stata trovata...
                msg="Nessuna Camera Trovata"
                # riporta a Main.html con un messaggio per la visualizzazione di un messaggio
                return render(request, "Main.html", {'form': formRicerca,'msg':msg})
            else:
                # se almeno una camera è stata trovata
                servizi=Servizio.objects.all()
                serviziDisponibili=ServiziDisponibili.objects.all()
                return render(request,"ListaCamereDisponibili.html",{'camere':camerelibere,'serviziDisponibili':serviziDisponibili,'servizi':servizi,'dataArrivo':dataArrivo,'dataPartenza':dataPartenza})
        else:
            # se nessuna Camera è stata trovata...
            msg = "Attenzione: Parametri di ricerca errati."
            # riporta a Main.html con un messaggio per la visualizzazione di un messaggio
            return render(request, "Main.html", {'form': formRicerca, 'msg': msg})

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