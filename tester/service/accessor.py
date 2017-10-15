from colorama import Fore

from tester.service.web_service import WebService
from tester.utils.http_utils import get_raw


class Accessor(WebService):
    def __init__(self, conf: dict) -> None:
        super().__init__(conf)

    def check_measurements(self, sensor_id: str, metrics: list) -> bool:
        print('Checking measurements', end=' ')
        temperature = self.measurements(sensor_id)
        if temperature is None:
            return False
        if max(metrics) != temperature['maxLast30Days']:
            print(Fore.RED + 'Max temperature mismatch')
            print('Expected ' + max(metrics) + ', but got ' + temperature['maxLast30Days'])
            return False
        avg_expected = sum(metrics)/float(len(metrics))
        if avg_expected != temperature['averageLast7Days']:
            print(Fore.RED + 'Average temperature for last 7 days mismatch')
            print('Expected ' + max(avg_expected) + ', but got ' + temperature['averageLast7Days'])
            return False
        if avg_expected != temperature['averageLastHour']:
            print(Fore.RED + 'Average temperature for last hour days mismatch')
            print('Expected ' + max(avg_expected) + ', but got ' + temperature['averageLastHour'])
            return False
        print(Fore.GREEN + 'OK')
        return True

    def check_events(self, sensor_id: str, events: list) -> bool:
        print('Checking events', end=' ')
        events_got = self.events(sensor_id)
        if events_got is None:
            return False
        temp_events = [e['temperature'] for e in events_got['events']]
        if temp_events != events:
            print(Fore.RED + 'Events temperature mismatch')
            print('Expected ' + str(events) + ', but got ' + str(temp_events))
            return False
        print(Fore.GREEN + 'OK')
        return True

    def measurements(self, sensor_id) -> dict or None:
        return get_raw(self.url + '/api/v1/sensors/' + sensor_id + '/measurements')

    def events(self, sensor_id) -> dict or None:
        return get_raw(self.url + '/api/v1/sensors/' + sensor_id + '/events')
