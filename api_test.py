# -*- coding: utf-8 -*-

import requests


BASE_URL = "http://127.0.0.1:5000/"

response = requests.get(BASE_URL + "api/df/" + "원내대표")
print(response.json())

response = requests.get(BASE_URL + "api/df", {"term": "원내대표"})
print(response.json())
