import os
from celery import Celery

# Imposta le variabili di ambiente per Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Crea l'app Celery
app = Celery("app")

# Configura Celery per usare le impostazioni di Django con prefisso "CELERY_"
app.config_from_object("django.conf:settings", namespace="CELERY")

# Cerca automaticamente le task in tutti i file tasks.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
