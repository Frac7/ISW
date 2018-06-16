#Test di accettazione per user story aggiungi camera
from GestioneHotel.models import *
from django.test import TestCase, Client
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
        # Indirizzo hotel
        indirizzo = Indirizzo(via="Via Ospedale", numero="72")
        indirizzo.save()
        # Hotel in cui e' presente la camera
        self.hotel = Hotel(nome="unHotel", descrizione="unHotelACagliari", citta="Cagliari", indirizzo=indirizzo, proprietario=self.albergatore)
        self.hotel.save()
        # crea una camera con dei dati
        # Camera(numero, posti letto, servizi, hotel)
        self.camera = Camera(numero=1, postiLetto=4, hotel=self.hotel)
        self.camera.save()
        # Servizi a disposizione per la camera
        servizi = ServiziDisponibili(camera=self.camera, servizio=servizio)
        servizi.save()
    #Task login user story, requisito
    def testLogin(self):
        #Controlla che i dati inseriti siano validi per il login
        tuttiGliAlbergatori = Albergatore.objects.all()
        self.assertEqual(self.albergatore.email, tuttiGliAlbergatori.get(id=self.albergatore.id).email)
        self.assertEqual(self.albergatore.password, tuttiGliAlbergatori.get(id=self.albergatore.id).password)
        #TODO: inserire da qualche parte autorizza accesso; Test provvisorio
        #TestLogin con Client
        #client = Client()
        #Si manda una richiesta post per il login con i dati
        #response = client.post("/Login.html/", {"email": self.albergatore.email, "password": self.albergatore.password})
        #La risposta deve essere 200 (e' andata a buon fine) - 302: redirection
        #self.assertEqual(response.status_code, 200)
        #Altre prove
        #response = client.post("/Login.html/", {"email": self.albergatore.email, "password": "passwordDiversa"})
        #Accesso negato
        #self.assertNotEqual(response.status_code, 403)

    #task aggiungi camera, requisito user story
    def testAggiungiCamera(self):
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        camera = Camera.objects.all().get(id=self.camera.id)
        #Controlla che la camera sia inserita nell'hotel (attributo hotel di camera)
        self.assertEqual(camera.hotel, self.hotel, "Camera non aggiunta")
        #Controlla che la camera creata sia la stessa che si ottiene filtrando per hotel
        self.assertEqual(Camera.objects.all().get(id=self.camera.id), Camera.objects.filter(hotel=self.hotel).get(id=self.camera.id))
        #Controlla che gli attributi della camera ottenuta dal filtro hotel siano uguali a quelli della camera creata
        camere = Camera.objects.filter(hotel=self.hotel)
        for camera in camere:
            self.assertEqual(camera, self.camera)

if __name__ == "__main__":
    unittest.main()
