import requests
from settings import proverkacheka_api, proverkacheka_token


def get_by_qrraw(qrraw: str) -> dict:
    data = {'token': proverkacheka_token, 'qrraw': qrraw}
    response = requests.post(proverkacheka_api, data=data).json()
    return response


def get_by_qrfile(qrfile) -> dict:
    data = {'token': proverkacheka_token}
    files = {'qrfile': qrfile}
    response = requests.post(proverkacheka_api, data=data, files=files).json()
    return response


def get_by_qrurl(qrurl: str) -> dict:
    data = {'token': proverkacheka_token, 'qrurl': qrurl}
    response = requests.post(proverkacheka_api, data=data).json()
    return response
  
