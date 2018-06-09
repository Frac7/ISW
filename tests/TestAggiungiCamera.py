#test di accettazione per user story aggiungi camera
class TestAggiungiCamera:
    #Task login user story, requisito
    def testLogin(self):
        #TODO: questo test sembra piu' adatto al requisito di registrazione
        #TODO: per il requisito di registrazione si potrebbe effettuare una verifica diversa (ad esempio, la presenza
        #TODO: dell'utente nel db)
        #Creazione albergatore (nome, cognome, email, password
        email = "username@dominio"
        password = "unaPassword"
        albergatore = Utente("un", "Albergatore", email, password)
        #Controlla che i dati inseriti siano validi per il login
        assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())
    #task aggiungi camera, requisito user story
    def testAggiungiCamera(self):
        #Creazione singolo servizio: nome e descrizione
        servizio = Servizio("TV", "televisione")
        #Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        #Indirizzo hotel
        indirizzo = Indirizzo("Via Ospedale", "72")
        #Hotel in cui e' presente la camera
        hotel = Hotel("unHotel", "unHotelACagliari", "Cagliari", indirizzo)
        #crea una camera con dei dati
        #Camera(numero, posti letto, servizi, hotel)
        camera = Camera(1, 4, servizi, hotel)
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        assert camera in hotel.listaCamere()

