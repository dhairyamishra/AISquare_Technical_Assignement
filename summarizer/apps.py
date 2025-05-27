from django.apps import AppConfig
from django.utils.module_loading import import_string

def ready(self):
    import_string('summarizer.signals')  # ensures signal is loaded

class SummarizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'summarizer'
