from tester.service.web_service import WebService
from tester.utils.http_utils import post


class Receiver(WebService):
    def report(self, sensor_uuid: str, metric: dict) -> dict or None:
        return post(self.url + '/api/v1/sensors/' + sensor_uuid + '/measurements', metric)
