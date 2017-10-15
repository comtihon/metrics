import redis


class Redis:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._host = conf['host']
        self._port = int(conf['port'])

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def get_events_counter(self, sensor_id: str) -> int or None:
        connection = redis.StrictRedis(host=self.host, port=self.port)
        events_num = connection.get(sensor_id)
        if events_num is None:
            return None
        return int(events_num)
