from django import forms

#Collegato alla view aggiungiCamera
class AggiungiCameraForm(forms.Form):
    numeroCamera = forms.CharField(label="numero",max_length=15,required=True)
    postiLettoCamera = forms.IntegerField(label="postiLetto",required=True)
    #TODO: servizi
    #L'hotel a cui viene aggiunta la camera e' presente nella query string