from django.apps import AppConfig
from ticketing.nlp.ml_model_loader import load_classifier



class TicketingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketing'

    def ready(self):
        # print("load")
        # load_classifier()
        # print("end")
        pass