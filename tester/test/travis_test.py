from tester.test.full import FullTest


# Same as FullTest but without kafka
class TravisTest(FullTest):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)
        self._name = __name__.split('.')[-1:][0]

    def check_kafka(self, sensor_id: str, events_temperature: list) -> bool:
        return True
