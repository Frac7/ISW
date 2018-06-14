#test di accettazione per user story aggiungi camera
from GestioneHotel.models import Albergatore, Servizio, Indirizzo, Hotel, Camera
from django.test import TestCase
import unittest

class TestAggiungiCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio(nome="TV", descrizioneServizio="televisione")
        servizio.save()
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario_id=self.albergatore.id)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, servizi_id=servizio.id, hotel_id=self.hotel.id)
        self.camera.save()
    #Task login user story, requisito
    def testLogin(self):
        #Controlla che i dati inseriti siano validi per il login
        self.assertTrue(Albergatore.autorizzaAccesso(self.albergatore.getEmail(), self.albergatore.getPassword()), 'Accesso non autorizzato')
    #task aggiungi camera, requisito user story
    def testAggiungiCamera(self):
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        self.assertTrue(self.camera in self.hotel.listaCamere(), 'Camera non aggiunta')

if __name__ == "__main__":
    unittest.main()
