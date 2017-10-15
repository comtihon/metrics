import requests
from colorama import Fore
from requests import Response
from requests.exceptions import ConnectionError


def get(url: str):
    try:
        r = requests.get(url=url)
        return response(r)
    except (ConnectionError, ConnectionRefusedError) as err:
        print(Fore.RED + 'Fail with ' + str(err))
        return None


def get_raw(url: str) -> dict or None:
    try:
        r = requests.get(url=url)
        if r is not None and r.status_code == 200:
            return r.json()
        return None
    except (ConnectionError, ConnectionRefusedError) as err:
        print(Fore.RED + 'Fail with ' + str(err))
        return None


def post(url: str, body: dict or list):
    try:
        r = requests.post(url=url, json=body)
        return response(r)
    except (ConnectionError, ConnectionRefusedError) as err:
        print(Fore.RED + 'Fail with ' + str(err))
        return None


def response(r: Response):
    if r.status_code == 200:
        return r.json()['response']
    else:
        print(Fore.RED + 'Fail with ' + str(r.status_code))
        return None
