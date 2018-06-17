from django import forms

#Collegato alla view aggiungiCamera
class AggiungiCameraForm(forms.Form):
    numeroCamera = forms.CharField(label="numero",max_length=15,required=True)
    postiLettoCamera = forms.IntegerField(label="postiLetto",required=True)
    #TODO: servizi
    #L'hotel a cui viene aggiunta la camera e' presente nella query string

class RegistrazioneAlbergatore(forms.Form):
    nome = forms.CharField(label="nome", max_length=50,required=True)
    cognome = forms.CharField(label="cognome", max_length=50,required=True)
    email = forms.EmailField(label="email", max_length=50,required=True)
    password = forms.CharField(label="password", max_length=32,required=True)