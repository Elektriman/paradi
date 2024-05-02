import unittest
from unittest import TestCase
import requests
from paradi import Paradi


class TestParadiClass(Paradi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _save_auth(self,
                   response: requests.Response
                   ):
        if response.status_code == 200:
            self.auth = {"auth_saved": True}


test_paradi_instance = TestParadiClass(entry="https://http.cat/",
                                       login_uri="",
                                       logout_uri="",
                                       login_kwargs={})


class TestParadi(TestCase):

    def test_instantiate(self):
        self.assertRaises(TypeError, Paradi.__new__)

    def test__request(self):

        def try_to_use_private_method():
            return test_paradi_instance.__request("GET", "200")

        self.assertRaises(AttributeError, try_to_use_private_method)

    def test_get(self):
        self.assertEqual(test_paradi_instance.get("200").status_code, 200)

    def test_post(self):
        self.assertEqual(test_paradi_instance.post("200").status_code, 200)

    def test__save_auth(self):
        response = test_paradi_instance.post("200")
        test_paradi_instance._save_auth(response=response)
        self.assertIsNotNone(test_paradi_instance.auth)
