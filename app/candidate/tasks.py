import re
from celery import shared_task
from core.models import Candidate
from random import randint
from requests import post


@shared_task(bind=True)
def run_screening(self, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    print("Va in esecuzione")
    if candidate:
        try:
            # Prendo un dizionario con qualche dato randomico, tipo lo score
            screening_log = screening()

            # Verifica se la mail è valida
            is_valid_email = is_email(candidate.email)
            screening_log["Email"] = "Valid email"
            if not is_valid_email:
                screening_log["Email"] = "Not valid email"

            # Verifica se l'account è un duplicato
            is_duplicated_account = is_duplicated(candidate.email)
            screening_log["Account"] = "The account is not a duplicate"
            if is_duplicated_account:
                screening_log["Account"] = "The account turns out to be a duplicate"

            if is_valid_email and not is_duplicated_account:
                candidate.status = "checked"
                screening_log["Blacklist"] = "false"
            else:
                candidate.status = "reject"
                screening_log["Blacklist"] = "true"
            print(screening_log)
            candidate.screening_log = screening_log
            candidate.save()

        except Exception as ex:
            print(ex.__str__())

            # Se ci saranno degli errori ritenterà l'esecuzione per un massimo di 3 volte dope 10 secondi
            raise self.retry(exc=ex, countdown=10, max_retries=3)

        send_to_azure(candidate)


def screening():
    return {
        "score": randint(1, 100),
        "notes": "Screening completato con successo",
    }


def is_email(email: str):
    valid_email = re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is not None
    return valid_email


def is_duplicated(email: str):
    fetched_data = list(Candidate.objects.filter(email=email))

    if len(fetched_data) > 1:
        return True
    return False


def send_to_azure(candidate_data):
    print("Il candidato è stato salvato su Azure")


@shared_task
def test_task(candidate: Candidate):
    header: dict = {"Content-Type": "application-json"}
    body: dict = {
        "candidate_id": candidate.id,
        "status": candidate.status,
        "screening_result": candidate.screening_log,
    }
    try:
        post(url="http://azure-mock.local/api/events", headers=header, json=body)
    except Exception as ex:
        print(ex.__str__())
