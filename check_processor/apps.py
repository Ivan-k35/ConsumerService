import threading
from django.apps import AppConfig


class CheckProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'check_processor'
    verbose_name = 'Обработчик чеков'

    def ready(self):
        consumer_thread = threading.Thread(target=self.run_kafka_consumer)
        consumer_thread.daemon = True
        consumer_thread.start()

    def run_kafka_consumer(self):
        from .consumers import kafka_consumer_function
        kafka_consumer_function()
