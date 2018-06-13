#test di accettazione per user story aggiungi camera
from GestioneHotel.models import Albergatore, Servizio, Indirizzo, Hotel, Camera
from django.test import TestCase
import unittest

class TestAggiungiCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        self.albergatore = Albergatore("un", "Albergatore", email, password)
        self.albergatore.save()
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio("TV", "televisione")
        servizio.save()
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo("Via Ospedale", "72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel("unHotel", "unHotelACagliari", "Cagliari", indirizzo, self.albergatore)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(1, 4, servizi, self.hotel)
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
