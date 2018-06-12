#test di accettazione per user story aggiungi camera
from GestioneHotel.models import Albergatore
from django.test import TestCase
import unittest

class TestAggiungiCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        albergatore = Albergatore("un", "Albergatore", email, password)
        self.albergatore = albergatore
        # Creazione singolo servizio: nome e descrizione
        servizio = Servizio("TV", "televisione")
        # Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        # Indirizzo hotel
        indirizzo = Indirizzo("Via Ospedale", "72")
        # Hotel in cui e' presente la camera
        hotel = Hotel("unHotel", "unHotelACagliari", "Cagliari", indirizzo, albergatore)
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        camera = Camera(1, 4, servizi, hotel)
        self.camera = camera
    #Task login user story, requisito
    def testLogin(self):
        #Controlla che i dati inseriti siano validi per il login
        self.assertTrue(autorizzaAccesso(self.albergatore.getEmail(), self.albergatore.getPassword()), 'Accesso non autorizzato')
    #task aggiungi camera, requisito user story
    def testAggiungiCamera(self):
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        self.assertTrue(self.camera in hotel.listaCamere(), 'Camera non aggiunta')

if __name__ == "__main__":
    unittest.main()
