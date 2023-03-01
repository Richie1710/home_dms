import factory
from .models import Device
from django.utils import timezone
import arrow
import random

GUARANTEE_TIME = [
    12,
    24,
    36,
    60,
    72,
]


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Device

    manufacturer = factory.Faker("company")
    name = factory.Faker("domain_word")
    serial_number = factory.LazyFunction(
        lambda: factory.Faker("isbn13")._get_faker().isbn13()
        if bool(random.getrandbits(1)) is True
        else None
    )
    buyed_at = factory.Faker(
        "date_time_between",
        start_date=arrow.utcnow().shift(days=-365).datetime,
        end_date=arrow.utcnow().shift(days=-60).datetime,
        tzinfo=timezone.get_current_timezone(),
    )
    guarantee_end = factory.Faker(
        "date_time_between",
        start_date=arrow.utcnow().shift(days=-60).datetime,
        end_date=arrow.utcnow().shift(days=60).datetime,
        tzinfo=timezone.get_current_timezone(),
    )
