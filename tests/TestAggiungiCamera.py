#test di accettazione per user story aggiungi camera
class TestAggiungiCamera:
    def testAggiungiCamera(self):
        #Creazione singolo servizio: nome e descrizione
        servizio = Servizio('TV', 'televisione')
        #Servizi a disposizione per la camera
        servizi = []
        servizi.append(servizio)
        #Indirizzo hotel
        indirizzo = Indirizzo('Via Ospedale', '72')
        #Hotel in cui e' presente la camera
        hotel = Hotel('unHotel', 'unHotelACagliari', 'Cagliari', indirizzo)
        #crea una camera con dei dati
        #Camera(numero, posti letto, servizi, hotel)
        camera = Camera(1, 4, servizi, hotel)
        #Una volta creata la camera, si controlla che questa sia presente nell'hotel
        assert camera in hotel.listaCamere()

