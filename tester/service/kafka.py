import json
from time import sleep

from colorama import Fore
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord


class Kafka:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._host = conf['host']
        self._port = str(conf['port'])
        self._topic_temperature = conf['topic_temperature']
        self._topic_events = conf['topic_events']

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    @property
    def topic_temperature(self) -> str:
        return self._topic_temperature

    @property
    def topic_events(self) -> str:
        return self._topic_events

    def connect_consumer(self, host, port, topic, retry=True):
        try:
            return KafkaConsumer(topic,
                                 group_id='tester',
                                 bootstrap_servers=host + ':' + port,
                                 auto_offset_reset='earliest',
                                 api_version=(0, 10, 1))
        except:
            if retry:
                sleep(5)
                return self.connect_consumer(host, port, topic, False)
            print(Fore.RED + 'No kafka brokers available')
            raise Exception('No kafka brokers available')

    def check_events(self, sensor_id: str, events: list) -> bool:
        print('Checking events in kafka', end=' ')
        return self.check(sensor_id, events, self.topic_events)

    def check_metrics(self, sensor_id: str, metrics: list) -> bool:
        print('Checking metrics in kafka', end=' ')
        return self.check(sensor_id, metrics, self.topic_temperature)

    def check(self, sensor_id: str, to_check: list, topic: str) -> bool:
        consumer = self.connect_consumer(self.host, self.port, topic)
        streamed_metrics = Kafka.get_messages(consumer)
        if streamed_metrics is None or streamed_metrics == {}:
            print(Fore.RED + 'No data streamed to kafka')
            return False
        for t in to_check:
            if t not in streamed_metrics[sensor_id]:
                print(Fore.RED + 'No ' + str(t) + ' in kafka')
                print(streamed_metrics)
                return False
        print(Fore.GREEN + 'OK')
        return True

    @staticmethod
    def get_messages(consumer) -> dict:
        consumer_records = consumer.poll(10000).values()
        records = [item for sublist in consumer_records for item in sublist]
        list_of_dicts = [Kafka.parse_value(c) for c in records]
        streamed = {}
        for d in list_of_dicts:
            if d['sensorUuid'] in streamed:
                streamed[d['sensorUuid']].append(d['temperature'])
            else:
                streamed[d['sensorUuid']] = [d['temperature']]
        return streamed

    @staticmethod
    def parse_value(c: ConsumerRecord) -> dict:
        return json.loads(c.value.decode())
