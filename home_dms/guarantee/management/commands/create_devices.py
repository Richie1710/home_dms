from django.core.management.base import BaseCommand

from guarantee.models import Device
from guarantee.factories import DeviceFactory


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            help="Number of Devices to be generated",
            required=True,
        )
        parser.epilog = "User: python manage.py create_devices -n 20"

    def handle(self, *args, **kwargs):
        print("numbers of devices:", kwargs.get("number"))

        n = kwargs.get("number")

        # all User bis auf username=admin löschen

        print("Deleting devices")
        Device.objects.all().delete()
        DeviceFactory.create_batch(n)
