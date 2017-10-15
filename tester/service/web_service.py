class WebService:
    def __init__(self, conf: dict) -> None:
        super().__init__()
        self._url = 'http://' + conf['host'] + ':' + str(conf['port'])

    @property
    def url(self) -> str:
        return self._url
