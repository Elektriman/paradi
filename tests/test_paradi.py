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
        self.auth = {}


test_paradi_instance = TestParadiClass(entry="https://http.cat/",
                                       login_uri="",
                                       logout_uri="",
                                       login_kwargs={})


class TestParadi(TestCase):

    def test_instantiate(self):
        self.assertRaises(TypeError, Paradi.__new__)

    def test__request(self):
        def try_to_use_private_method():
            test_paradi_instance.__request("GET", "https://http.cat/")

        self.assertRaises(AttributeError, try_to_use_private_method)

    def test_get(self):
        self.fail()

    def test_post(self):
        self.fail()

    def test__save_auth(self):
        self.fail()
