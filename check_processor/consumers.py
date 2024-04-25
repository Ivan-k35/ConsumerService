import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from .serializers import PurchaseSerializer
from .models import Place
from loguru import logger


def kafka_consumer_function():
    bootstrap_servers = 'kafka:9092'
    topic = 'purchase_checks'

    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

    topics_metadata = admin_client.list_topics(timeout=10)
    if topic not in topics_metadata.topics:
        new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])

    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'my_consumer_group',
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    logger.info('Kafka consumer started')

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.warning('Достигнут конец раздела {0} [{1}]'.format(msg.topic(), msg.partition()))
                elif msg.error():
                    logger.error('Ошибка при получении сообщения: {0}'.format(msg.error()))
                continue

            try:
                data = json.loads(msg.value().decode('utf-8'))
                logger.info('Received message: {0}'.format(data))
                serializer = PurchaseSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    place, created = Place.objects.get_or_create(place_id=data['place_id'],
                                                                 defaults={'place_name': data['place_name']})
                    if not created:
                        place.place_name = data['place_name']
                        place.save()

                else:
                    logger.error('Неверные данные, полученные из Kafka: {0}'.format(serializer.errors))
            except Exception as e:
                logger.exception('Ошибка обработки сообщения Kafka: {0}'.format(e))
    finally:
        consumer.close()
