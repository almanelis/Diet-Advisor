import os

import requests
from dotenv import load_dotenv

load_dotenv()

PROVERCKACHECKA_API = os.getenv('PROVERCKACHECKA_API')
PROVERCKACHECKA_TOKEN = os.getenv('PROVERCKACHECKA_TOKEN')


def get_by_qrraw(qrraw: str) -> dict:
    data = {'token': PROVERCKACHECKA_TOKEN, 'qrraw': qrraw}
    response = requests.post(PROVERCKACHECKA_API, data=data).json()
    return response


def get_by_qrfile(qrfile: str) -> dict:
    data = {'token': PROVERCKACHECKA_TOKEN}
    files = {'qrfile': qrfile}
    response = requests.post(PROVERCKACHECKA_API,
                             data=data, files=files).json()
    return response


def get_by_qrurl(qrurl: str) -> dict:
    data = {'token': PROVERCKACHECKA_TOKEN, 'qrurl': qrurl}
    response = requests.post(PROVERCKACHECKA_API, data=data).json()
    return response
