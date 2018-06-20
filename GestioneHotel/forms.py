from django import forms
from GestioneHotel.models import *

#Collegato alla view aggiungiCamera
class AggiungiCameraForm(forms.Form):
    numero = forms.CharField(label="Numero",max_length=15,required=True,widget=forms.TextInput(attrs={'id': 'campoCamera'}))
    elencoPosti = [(i, i) for i in range(1, 7)]
    postiLetto = forms.ChoiceField(label="Posti Letto", choices=elencoPosti)
    servizio1 = forms.BooleanField(required=False,label="TV",widget=forms.CheckboxInput(attrs={'id': 'servizioCamera'}))
    servizio2 = forms.BooleanField(required=False,label="Aria condizionata",widget=forms.CheckboxInput(attrs={'id': 'servizioCamera'}))
    servizio3 = forms.BooleanField(required=False,label="Frigo bar",widget=forms.CheckboxInput(attrs={'id': 'servizioCamera'}))

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email",required=True)
    password = forms.CharField(label="Password",required=True,widget=forms.PasswordInput)

class RegistrazioneAlbergatore(forms.Form):
    nome = forms.CharField(label="nome", max_length=50,required=True)
    cognome = forms.CharField(label="cognome", max_length=50,required=True)
    email = forms.EmailField(label="email", max_length=50,required=True)
    password = forms.CharField(label="password", max_length=32,required=True)

class AggiungiHotelForm(forms.Form):
     nome = forms.CharField(label="Nome", max_length=30, required=True,
                               widget=forms.TextInput(attrs={'id': 'nomeHotel'}))
     descrizione = forms.CharField(label='Descrizione', max_length=100, required=True,
                                      widget=forms.TextInput(attrs={'id': 'descrizioneHotel'}))
     citta = forms.CharField(label='Citta', max_length=30, required=True,
                                widget=forms.TextInput(attrs={'id': 'cittaHotel'}))
     via = forms.CharField(label='Via', max_length=50, required=True,
                              widget=forms.TextInput(attrs={'id': 'viaHotel'}))
     numeroCivico = forms.CharField(label='NumeroCivico', max_length=10, required=True,
                                       widget=forms.TextInput(attrs={'id': 'numeroHotel'}))

class FormRicerca(forms.Form):

    #recupero l'elenco delle citta dagli hotel
    elencoCitta = [(hotel.citta, hotel.citta) for hotel in Hotel.objects.order_by('citta')]
    # html select della citta dell'elenco delle citta disponibili
    citta=forms.ChoiceField(label="Destinazione",widget=forms.Select, choices=elencoCitta)
    # input data arrivo
    dataArrivo = forms.DateField(label="Arrivo",widget=forms.SelectDateWidget())
    #input data partenza
    dataPartenza = forms.DateField(label="Partenza",widget=forms.SelectDateWidget())
    elencoPosti=[(i,i) for i in range(1, 7)]
    posti = forms.ChoiceField(label="Posti",choices=elencoPosti)

class FormPrenota(forms.Form):
    # input dell'indirizzo Email dell'utente che effettua la prenotazione
    prenotaUtente = forms.EmailField(label="Email")
    prenotaCheckin = forms.CharField(widget=forms.HiddenInput())
    prenotaCheckout = forms.CharField(widget=forms.HiddenInput())
    prenotaIdCamera = forms.CharField(widget=forms.HiddenInput())
