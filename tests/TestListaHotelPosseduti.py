#test di accettazione per la user story, visualizza la lista prenotazioni
class TestListaPrenotazioni
    #task login user login, requisito
    def testLogin(self):
        #Creazione albergatore (nome, cognome, email, password
        email = "user@name"
        password = "password"
        albergatore = Utente("Pippo", "Albergatore", email, password)
        #Controlla che i dati inseriti siano validi per il login
        assert autorizzaAccesso(albergatore.getEmail(), albergatore.getPassword())

    #Una volta ch'e' stato effettuato il login, l'untente tramite il menu accede alla lista degli hotel che li appartengono
    #          e controlla se ci sono presenti tutti