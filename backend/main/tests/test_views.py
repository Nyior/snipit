from rest_framework.test import APITestCase

from main.models import Url
from main.api.views import shorten_url

from django.urls import reverse
import json


class SetUpClass(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        this method sets up the data to be used across 
        multiple classses"""

        cls.url = Url.objects.create(
                                    long_url="https://nyior-clement.netlify.app/",
                                    shortcode="xxbb5t")
        cls.valid_payload = {
                            "longUrl": "https://nyior-clement.netlify.app/",
                            "shortcode": "xxbb5"
                        }
        cls.invalid_payload = {
                            "longUrl": "https://nyior-clement.netlify.app/"
                            }


class ShortenUrlView(SetUpClass):
    """ This tests the shorten url function"""  
    global route
    route = reverse("shorten-url")           

    def test_view_returns_status_ok(self):
        """tests if view always return an ok response"""

        resp = self.client.post(
                                route, 
                                self.valid_payload, 
                                format='json')
        resp2 = self.client.post(
                                    route, 
                                    self.invalid_payload, 
                                    format='json')  

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

    def test_view_returns_shortcode(self):
        """tests if shortcode is in the response returned
        the goal is to test the functionality of creating custom
        urls. """

        resp = self.client.post(
                                route, 
                                self.valid_payload, 
                                format='json')

        self.assertEqual(resp.data, self.valid_payload)

    def test_shortcode_isnot_null(self):
        """tests that the value of the shortcode returned is not null
        the goal is to test the functionality of system generated 
        short urls. 
        """
        resp = self.client.post(
                                    route, 
                                    self.invalid_payload, 
                                    format='json')  

        self.assertTrue(resp.data["shortcode"] is not None)
        


class TestRedirectView(SetUpClass):
    """this class tests the redirect view function"""

    def test_view_returns_302(self):
        shortcode = self.url.shortcode
        route = reverse("redirect", args=[shortcode])

        resp = self.client.get(route)

        self.assertEqual(resp.status_code, 302)

    def test_view_redirects_to_original_url(self):
        shortcode = self.url.shortcode
        route = reverse("redirect", args=[shortcode])

        resp = self.client.get(route)

        self.assertRedirects(
                                resp, 
                                self.url.long_url, 
                                fetch_redirect_response=False)


class TestUrlStatsView(SetUpClass):
    """this class tests the view that returns some stats about a url"""

    def test_view_returns_200(self):
        shortcode = self.url.shortcode
        route = reverse("url-stats", args=[shortcode])

        resp = self.client.get(route)

        self.assertEqual(resp.status_code, 200)

    def test_expected_params_in_response(self):
        shortcode = self.url.shortcode
        route = reverse("url-stats", args=[shortcode])

        resp = self.client.get(route)

        self.assertContains(resp, "dateCreated")
        self.assertContains(resp, "lastAccessed")
        self.assertContains(resp, "hits") 


class TestGetClientUrlsView(SetUpClass):
    """this class tests the view that returns a list of all the 
    urls shortened by a client"""

    def test_view_returns_200(self):
        shortcode = self.url.shortcode
        route = reverse("list-urls")

        resp = self.client.get(route)

        self.assertEqual(resp.status_code, 200)