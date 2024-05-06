from unittest import TestCase
import requests
from paradi import Paradi
import json
import threading
from flask_test_api import app


server = threading.Thread(target=app.run, name="server")

with open("http.json", "r") as f:
    http_dict = json.load(f)


class TestParadiClass(Paradi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _save_auth(self,
                   response: requests.Response
                   ):
        if response.status_code == 200:
            self.auth = {"auth_saved": True}


test_paradi_instance = TestParadiClass(entry="http://127.0.0.1:5000",
                                       login_uri="",
                                       logout_uri="",
                                       login_kwargs={})


class TestParadi(TestCase):
    @classmethod
    def setUpClass(cls):
        server.start()

    @classmethod
    def tearDownClass(cls):
        server.join()

    def test_instantiate(self):
        self.assertRaises(TypeError, Paradi.__new__)

    def test__request(self):
        global test_paradi_instance

        def try_to_use_private_method():
            return test_paradi_instance.__request("GET", "200")

        self.assertRaises(AttributeError, try_to_use_private_method)

    def test_get(self):
        global test_paradi_instance
        self.assertIsInstance(test_paradi_instance.get("http/200"), requests.Response)
        for status_code, message in http_dict.items():
            def try_request():
                return test_paradi_instance.get(f"http/{status_code}")

            if 200 <= int(status_code) < 300:
                self.assertEqual(try_request().status_code, int(status_code))
            else:
                self.assertRaises(Exception, try_request)

    def test_post(self):
        global test_paradi_instance
        test_request = test_paradi_instance.post("post/data")
        self.assertIsInstance(test_request, requests.Response)
        self.assertEqual(test_request.status_code, 200)

    def test__save_auth(self):
        global test_paradi_instance
        response = test_paradi_instance.post("post/data")
        test_paradi_instance._save_auth(response=response)
        self.assertIsNotNone(test_paradi_instance.auth)
