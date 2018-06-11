# Test di Accettazione per la Uesr Story Elenco Camere

from django.test import TestCase
class TestElencoCamere(TestCase):

    def testElecoCamere(self):
        albergatore=Albergatore("Nome","Cognome","email","password")
        hotel=Hotel("Hilton",albergaore)

        listacamere = []

        servizi={"FB":"Frigo-bar","AC":"Aria Condizionata"}
        camera1=Camera(hotel,1,servizi)
        listacamere.append(self,camera)

        servizi={"SK":"SKY","CF":"Cassaforte"}
        camera2=Camera(hotel,2,servizi)
        listacamere.append(self,camera)

        assert listacamere[0]==camera1
        assert listacamere[1] == camera2
            

