from time import sleep

from tester.test.full import FullTest


# Same as FullTest but without kafka
class TravisTest(FullTest):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self._name = __name__.split('.')[-1:][0]

    def check_kafka(self, sensor_id: str, events_temperature: list) -> bool:
        return True

    def check_redis(self, sensor_id: str) -> bool:
        sleep(5)
        return super().check_redis(sensor_id)

    def check_postgres(self, sensor_id: str) -> bool:
        sleep(5)
        return super().check_postgres(sensor_id)
