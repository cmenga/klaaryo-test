# Screening System - Setup & Usage

## Prerequisiti

- Docker e Docker Compose installati sulla tua macchina

---

## Avvio dell'ambiente

Per avviare tutti i servizi (Django, PostgreSQL, Redis, Celery):

```bash
docker-compose up --build
```

dopo bisogna creare l'utente per la JWT
- aprire un altro terminale o terminate l'esecuzione

```bash
docker-compose run --rm web sh -c "python manage.py createsuperuser"
```

### Sole se avete terminato l'esecuzione di docker-compose
Dopo aver creato l'utente bisogna ri-startare il docker-compose
```bash
docker-compose up
```

# Accesso all'API
L'API REST è disponibile all'indirizzo code .

```bash
http://127.0.0.1:8000/api/docs
```

Qui puoi vedere tutte le api tramite la dcuemntazione interattiva di Swagger/OpenAPI, per testare le singole chiamate.


# Note importanti
- Il backend è esposto sulla porta 8000, redis e postgres non sono esposti all'esterno.
- Celery e Redis sono configurati e avviati in automatico dal docker-compose
- La parte gRPC è configurata ma non funzionante a causa di problemi di import di candidate_pb2 

```bash
Could not import 'candidate.grpc.service.grpc_handlers' for GRPC setting 'ROOT_HANDLERS_HOOK'. ModuleNotFoundError: No module named 'candidate_pb2'.
```


# Esempio di utilizzo

All'interno del progetto c'è un file python chiamato example_usage.py, 
è possibile eseguire il file per effettare i vari test delle api e verificarne il funzionamente.
- prima di lanciare il comando ricordatevi di aggiornare le credenziali con il superuser che avete creato
  
```bash
py example_usage.py
```




