# -*- coding: utf-8 -*-

from http.client import responses
import requests
from sympy import re


BASE_URL = "http://127.0.0.1:5000/"

def test_get():
    # {'id': 20, 'term': '원내대표', 'frequency': 6, 'idf': 2.436116485618568}
    response = requests.get(BASE_URL + "api/df/" + "원내대표")
    print(response.json())

    # {'id': 20, 'term': '원내대표', 'frequency': 6, 'idf': 2.436116485618568}
    response = requests.get(BASE_URL + "api/df", {"term": "원내대표"})
    print(response.json())

def test_put():
    # {'id': 5049, 'term': '포켓몬', 'frequency': 5, 'idf': 2.5902671654458267}
    response = requests.put(BASE_URL + "api/df", {"term": "포켓몬", "frequency": 5})
    print(response.json())

    # 'id': 5050, 'term': '디지몬', 'frequency': 7, 'idf': 2.1}
    response = requests.put(BASE_URL + "api/df",
                            {"term": "디지몬", "frequency": 7, "idf": 2.1})
    print(response.json())

def test_patch():
    # {'id': 5049, 'term': '포켓몬', 'frequency': 6, 'idf': 2.5902671654458267}
    response = requests.patch(BASE_URL + "api/df", {"term": "포켓몬", "frequency": 6})
    print(response.json())

    # 'id': 5050, 'term': '디지몬', 'frequency': 5, 'idf': 2.3}
    response = requests.patch(
        BASE_URL + "api/df", {"term": "디지몬", "frequency": 5, "idf": 2.3})
    print(response.json())

def test_delete():
    # <Response [204]>
    response = requests.delete(BASE_URL + "api/df/" + "포켓몬")
    print(response)

    # <Response [204]>
    response = requests.delete(BASE_URL + "api/df/" + "디지몬")
    print(response)

def test_get_tfidf(text):
    response = requests.get(BASE_URL + "tfidf", {"text": text})
    print(response.json()[:5])

# test_get()
# test_put()
# test_patch()
# test_delete()
with open("text.txt", "r", encoding="utf-8") as f:
    text = f.readline()
test_get_tfidf(text)