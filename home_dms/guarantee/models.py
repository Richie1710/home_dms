from django.db import models
from django.urls import reverse
import arrow


class Device(models.Model):
    manufacturer = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30, blank=True, null=True)
    model = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="uploads/images",
        null=True,
        blank=True
    )
    buyed_at = models.DateField(default=arrow.utcnow().date)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    guarantee_end = models.DateField(
        default=arrow.utcnow().shift(years=2).date(),
    )
    proof_of_purchase = models.FileField(
        upload_to="uploads/purchase", null=True, blank=True
    )
    manual = models.FileField(
        upload_to="uploads/manuals",
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        name = f"{self.manufacturer},{self.name}"
        return name

    def get_absolute_url(self):
        return reverse("guarantee:guarantee_detail", kwargs={"pk": self.pk})

    def delete_absolute_url(self):
        return reverse("guarantee:guarantee_delete", kwargs={"pk": self.pk})

    def edit_absolute_url(self):
        return reverse("guarantee:guarantee_update", kwargs={"pk": self.pk})

    def check_guarantee(self):
        if self.guarantee_end >= arrow.utcnow().date():
            return True
        else:
            return False
