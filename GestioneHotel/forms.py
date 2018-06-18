from django import forms

#Collegato alla view aggiungiCamera
class AggiungiCameraForm(forms.Form):
    numeroCamera = forms.CharField(label="Numero",max_length=15,required=True,widget=forms.TextInput(attrs={'id' : 'campoCamera'}))
    postiLettoCamera = forms.IntegerField(label="Posti Letto",required=True,widget=forms.NumberInput(attrs={'id' : 'campoCamera'}))
    servizio1 = forms.BooleanField(required=False,label="TV",widget=forms.CheckboxInput(attrs={'id' : 'servizioCamera'}))
    servizio2 = forms.BooleanField(required=False,label="Aria condizionata",widget=forms.CheckboxInput(attrs={'id' : 'servizioCamera'}))
    servizio3 = forms.BooleanField(required=False,label="Frigo bar",widget=forms.CheckboxInput(attrs={'id' : 'servizioCamera'}))

class RegistrazioneAlbergatore(forms.Form):
    nome = forms.CharField(label="nome", max_length=50,required=True)
    cognome = forms.CharField(label="cognome", max_length=50,required=True)
    email = forms.EmailField(label="email", max_length=50,required=True)
    password = forms.CharField(label="password", max_length=32,required=True)