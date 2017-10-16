from time import sleep

from tester.test.full import FullTest


# Same as FullTest but without kafka
class TravisTest(FullTest):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self._name = __name__.split('.')[-1:][0]

    def run(self) -> bool:
        sleep(50)
        return super().run()

    def check_kafka(self, sensor_id: str, events_temperature: list) -> bool:
        sleep(10)
        return True

    def check_redis(self, sensor_id: str) -> bool:
        sleep(10)
        return super().check_redis(sensor_id)

    def check_postgres(self, sensor_id: str) -> bool:
        sleep(10)
        return super().check_postgres(sensor_id)
