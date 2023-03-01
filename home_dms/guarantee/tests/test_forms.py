from django.test import Client, TestCase
from django.urls import reverse
from guarantee.models import Device
from http import HTTPStatus
import arrow


class DeviceFormsTests(TestCase):
    def setUp(self):
        """
        läuft VOR jeder Testmethode
        """
        self.client = Client()
        self.device_payload = {
            "manufacturer": "Test-Manufacturer",
            "name": "Test-Name",
            "buyed_at": "2023-03-01",
            "guarantee_end": "2024-03-01",
        }

    def test_add_Device_form_minimal(self):
        """Teste ob eine Kategorie per POST angelegt werden kann."""
        response = self.client.post(
            reverse("guarantee:guarantee_add"), self.device_payload
        )

        device = (
            Device.objects.filter(name=self.device_payload["name"])
            .filter(manufacturer=self.device_payload["manufacturer"])
            .exists()
        )
        self.assertTrue(device)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_Device_guarantee_end_before_buying(self):
        """Teste das kein Garantiedatum vor dem Kaufdatum gewählt werden kann"""
        self.device_payload["guarantee_end"] = "2022-03-01"
        response = self.client.post(
            reverse("guarantee:guarantee_add"), self.device_payload
        )
        self.assertEqual(
            "Das Ende der Garantie kann nicht vor dem Kaufdatum liegen",
            response.context_data["form"]._errors["guarantee_end"].data[0],
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_search_manufacturer(self):
        """Testet die Suchfunktion
        """
        self.client.post(
            reverse("guarantee:guarantee_add"), self.device_payload
        )

        searchurl = reverse("guarantee:guarantee_search")
        manufacturer = self.device_payload["manufacturer"]
        name = self.device_payload["name"]
        manufacturerresponse = self.client.get(
            f"{searchurl}?q={manufacturer}"
        )
        nameresponse = self.client.get(
            f"{searchurl}?q={name}"
        )
        negativeresponse = self.client.get(
            f"{searchurl}?q=NOTEXIST"
        )
        print(manufacturerresponse, nameresponse)
        self.assertContains(manufacturerresponse, text=manufacturer)
        self.assertContains(nameresponse, text=name)
        self.assertNotContains(negativeresponse, text=manufacturer)
        self.assertEqual(manufacturerresponse.status_code, HTTPStatus.OK)
        self.assertEqual(nameresponse.status_code, HTTPStatus.OK)

    def test_check_guarantee(self):
        """Teste ob eine Kategorie per POST angelegt werden kann."""

        truepayload = {
            "manufacturer": "true_Manufacturer",
            "name": "guarantee_true_",
            "buyed_at": arrow.utcnow().date(),
            "guarantee_end": arrow.utcnow().shift(days=2).date(),
        }

        falsepayload = {
            "manufacturer": "false_Manufacturer",
            "name": "guarantee_false",
            "buyed_at": arrow.utcnow().shift(years=-1).date(),
            "guarantee_end": arrow.utcnow().shift(days=-1).date(),
        }
        true_response = self.client.post(
            reverse("guarantee:guarantee_add"), truepayload
        )
        self.assertEqual(true_response.status_code, HTTPStatus.FOUND)
        false_response = self.client.post(
            reverse("guarantee:guarantee_add"), falsepayload
        )
        self.assertEqual(false_response.status_code, HTTPStatus.FOUND)
        true_device = (
            Device.objects.filter(name=truepayload["name"])
            .filter(manufacturer=truepayload["manufacturer"]).get()
        )
        self.assertTrue(true_device.check_guarantee())
        false_device = (
            Device.objects.filter(name=falsepayload["name"])
            .filter(manufacturer=falsepayload["manufacturer"]).get()
        )
        self.assertFalse(false_device.check_guarantee())
