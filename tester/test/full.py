import uuid
from time import sleep

from colorama import Fore

from tester.service.accessor import Accessor
from tester.service.kafka import Kafka
from tester.service.postgres import Postgres
from tester.service.receiver import Receiver
from tester.service.redis import Redis
from tester.test.test import Test


class FullTest(Test):
    def __init__(self, conf: dict) -> None:
        super().__init__(__name__)
        self._receiver = Receiver(conf['receiver'])
        self._postgres = Postgres(conf['postgres'])
        self._kafka = Kafka(conf['kafka'])
        self._redis = Redis(conf['redis'])
        self._accessor = Accessor(conf['accessor'])

    @property
    def metrics(self) -> list:
        return [10, 100, 97, 99, 10, 100, 107, 98]

    @property
    def events_t(self) -> list:
        return [99, 98]  # events have last measurement's temperature

    @property
    def receiver(self) -> Receiver:
        return self._receiver

    @property
    def postgres(self) -> Postgres:
        return self._postgres

    @property
    def kafka(self) -> Kafka:
        return self._kafka

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def accessor(self) -> Accessor:
        return self._accessor

    def run(self) -> bool:
        sleep(10)  # to wait for all services to be 100% ready
        sensor_id = str(uuid.uuid4())
        if not self._report_metrics(sensor_id):
            return False
        if not self.check_kafka(sensor_id, self.events_t):
            return False
        if not self.check_redis(sensor_id):
            return False
        if not self.check_postgres(sensor_id):
            return False
        if not self.check_accessor(sensor_id):
            return False
        return True

    def check_kafka(self, sensor_id: str, events_temperature: list) -> bool:
        if not self.kafka.check_metrics(sensor_id, events_temperature):
            return False
        if not self.kafka.check_events(sensor_id, events_temperature):
            return False
        return True

    def check_redis(self, sensor_id: str) -> bool:
        print('Checking events in redis', end=' ')
        events = self.redis.get_events_counter(sensor_id)
        if events is None:
            print(Fore.RED + "Fail, no events in redis")
            return False
        if events != 3:  # last 3 warnings from self.metrics
            print(Fore.RED + "Fail, got " + str(events) + " vs " + str(3))
            return False
        print(Fore.GREEN + "OK")
        return True

    def check_postgres(self, sensor_id: str) -> bool:
        return self.postgres.check_measurements(sensor_id, self.metrics, self.events_t)

    def check_accessor(self, sensor_id: str) -> bool:
        if not self.accessor.check_measurements(sensor_id, self.metrics):
            return False
        if not self.accessor.check_events(sensor_id, self.events_t):
            return False
        return True

    def _report_metrics(self, sensor: str) -> bool:
        print('Report metrics for ' + sensor, end=' ')
        for t in self.metrics:
            if self.receiver.report(sensor, {'temperature': t}) is None:
                return False
        print(Fore.GREEN + "OK")
        return True
