from time import sleep

import psycopg2
from colorama import Fore


class Postgres:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._conf = conf

    @property
    def conf(self) -> dict:
        return self._conf

    def check_measurements(self, sensor_id: str, temperature: list, events: list) -> bool:
        print('Checking temperature in postgres', end=' ')
        measurements = self.get_measurements(sensor_id)
        if measurements is None:
            return False
        (temperature_db, events_db) = measurements
        if temperature_db != temperature:
            print(Fore.RED + 'Temperature mismatch.')
            print('Reported ' + str(temperature) + "\nGot from db " + str(temperature_db))
            return False
        if events != events_db:
            print(Fore.RED + 'Events mismatch.')
            print('Reported ' + str(events) + "\nGot from db " + str(events_db))
            return False
        print(Fore.GREEN + 'OK')
        return True

    def get_measurements(self, sensor_id: str) -> tuple or None:
        try:
            conn = psycopg2.connect(host=self.conf['host'],
                                    port=self.conf['port'],
                                    database=self.conf['database'],
                                    user=self.conf['user'],
                                    password=self.conf['password'])
        except Exception as e:
            print(Fore.RED + 'Can\'t connect to postgres: ' + str(self.conf) + ' -> ' + e)
            return None
        cur = conn.cursor()
        temperature = Postgres.find_temperature(cur, sensor_id)
        if temperature is None:
            return None
        if not temperature:
            print(Fore.RED + 'No temperature for ' + sensor_id)
            return None
        events = Postgres.find_events(cur, sensor_id)
        if events is None:
            return None
        if not events:
            print(Fore.RED + 'No events for ' + sensor_id)
            return None
        return temperature, events

    @staticmethod
    def find_temperature(cur, sensor_id, retry=True) -> list or None:
        try:
            cur.execute("SELECT temperature from metrics where sensor_uuid='" + sensor_id + "'")
            res = [t[0] for t in cur.fetchall()]
            if not res and retry:
                sleep(1)
                return Postgres.find_temperature(cur, sensor_id, False)
            return res
        except Exception as e:
            print(Fore.RED + 'Can\'t query metrics for sensor_uuid: ' + sensor_id + ' -> ' + e)
            return None

    @staticmethod
    def find_events(cur, sensor_id, retry=True) -> list or None:
        try:
            cur.execute("SELECT temperature from event where sensor_uuid='" + sensor_id + "'")
            res = [t[0] for t in cur.fetchall()]
            if not res and retry:
                sleep(5)  # to wait for events
                return Postgres.find_events(cur, sensor_id, False)
            return res
        except Exception as e:
            print(Fore.RED + 'Can\'t query event for sensor_uuid: ' + sensor_id + ' -> ' + e)
            return None
