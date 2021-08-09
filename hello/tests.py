import json

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index, host, db
from .models import Greeting


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "index")

    def test_host(self):
        request = self.factory.get("/host")
        request.user = AnonymousUser()

        response = host(request)

        self.assertContains(response, "hostname")
        self.assertContains(response, "random_char")

    def test_db(self):
        request = self.factory.get("/host")
        request.user = AnonymousUser()
        response = db(request)

        self.assertEqual(Greeting.objects.count(), 1)

        self.assertContains(response, "count")
        self.assertContains(response, "data")

    def test_lang_none(self):
        request = self.factory.get("/host")
        request.user = AnonymousUser()
        response = db(request)

        response_j = json.loads(response.content)

        datas = response_j.get("data", [{}])
        data_element = datas[0]
        self.assertIn("when", data_element)
        self.assertEqual(None, data_element["exclamation"])
        self.assertEqual(None, data_element["exclamation_lang"])

    def test_lang_all(self):
        for i, lang in enumerate(Greeting.EXCLAMATION.names):
            requested_lang = lang.lower()
            expected_lang = Greeting.EXCLAMATION[lang]
            request = self.factory.get("/host", {"language": requested_lang})
            request.user = AnonymousUser()
            response = db(request)

            response_j = json.loads(response.content)
            datas = response_j["data"]
            # TODO: dont expect fixed ordering here
            data_element = datas[::-1][i]
            self.assertIn("when", data_element)
            self.assertEqual(expected_lang.value, data_element["exclamation"])
            self.assertEqual(expected_lang.name.lower(), data_element["exclamation_lang"])

    def test_lang_unknown(self):
        request = self.factory.get("/host", {"language": "Ankh-Morporkian"})
        request.user = AnonymousUser()
        response = db(request)

        self.assertEqual(400, response.status_code)