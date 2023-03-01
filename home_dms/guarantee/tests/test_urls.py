"""
Teste, ob GET Urls erreichbar sind.
"""
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from guarantee.factories import DeviceFactory


class EventUrlsTests(TestCase):
    def setUp(self):
        """
        läuft VOR jeder Testmethode
        """
        self.client = Client()
        self.event = DeviceFactory(manufacturer="testmanufacturer")

    def test_event_detail_page_is_public(self):
        """Prüfe, ob die Event-Detailseite public erreichbar ist."""
        url = reverse(
            "guarantee:guarantee_detail",
            kwargs={"pk": self.event.pk}
        )
        response = self.client.get(url)
        self.assertContains(response, text="testmanufacturer")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_event_list_page_is_public(self):
        """Prüfe, ob die Event-Detailseite public erreichbar ist."""
        url = reverse(
            "guarantee:guarantee_list"
        )
        response = self.client.get(url)
        self.assertContains(response, text="testmanufacturer")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_page_is_public(self):
        """Prüfe, ob die Event-Detailseite public erreichbar ist."""
        url = reverse(
            "guarantee:guarantee_delete",
            kwargs={"pk": self.event.pk}
        )
        response = self.client.get(url)
        self.assertContains(response, text="testmanufacturer")
        self.assertEqual(response.status_code, HTTPStatus.OK)
