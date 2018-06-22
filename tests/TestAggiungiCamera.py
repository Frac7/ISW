#Test di accettazione per user story aggiungi camera
from django.contrib.auth.models import User

from GestioneHotel.models import *
from django.test import TestCase, Client
import unittest

class TestAggiungiCamera(TestCase):
    def setUp(self):
        # Creazione albergatore (nome, cognome, email, password
        email = "username@dominio.it"
        password = "unaPassword"
        self.albergatore = Albergatore(nome="un", cognome="Albergatore", email=email, password=password)
        self.albergatore.save()
        #Creazione user a cui e' associato l'albergatore
        self.user = User(username=self.albergatore.email)
        self.user.set_password(password)
        self.user.save()
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
        #Creazione client
        self.client = Client()
        self.client.logout()
    #Task login user story, requisito
    def testModelsLogin(self):
        #Controlla che i dati inseriti siano validi per il login
        tuttiGliAlbergatori = Albergatore.objects.all()
        self.assertEqual(self.albergatore.email, tuttiGliAlbergatori.get(id=self.albergatore.id).email)
        self.assertEqual(self.albergatore.password, tuttiGliAlbergatori.get(id=self.albergatore.id).password)
        self.assertEqual(len(User.objects.all()), len(Albergatore.objects.all()))
    def testViewLogin(self):
        #Una volta fatto il login deve essere visualizzata la home
        response = self.client.post("/Login/",
                         {"email": self.albergatore.email, "password": self.albergatore.password},
                         follow=True)
        self.assertNotContains(response, "errati")
        self.assertContains(response, "prenotazioni")
    #task aggiungi camera, requisito user story
    def testModelsAggiungiCamera(self):
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
    def testViewAggiungicamera(self):
        # Una volta fatto il login deve essere visualizzata la home
        self.client.post("/Login/",
                                    {"email": self.albergatore.email, "password": self.albergatore.password},
                                    follow=True)
        #Da qui si passa alla lista hotel
        response = self.client.get("/AggiungiHotel/" + str(self.albergatore.id) + "/")
        self.assertContains(response, self.hotel.nome)
        self.assertContains(response, len(self.hotel.listaCamere()))
        #Da qui si sceglie l'hotel al quale aggiungere la camera
        response = self.client.get("/InfoHotelAggiungiCamera/" + str(self.hotel.id) + "/")
        self.assertContains(response, self.camera.numero)
        self.assertContains(response, self.camera.postiLetto)
        for servizioDisponibile in self.camera.listaServizi():
            for servizio in servizioDisponibile:
                self.assertContains(response, servizio.nome)
                self.assertContains(response, servizio.descrizioneServizio)

if __name__ == "__main__":
    unittest.main()
