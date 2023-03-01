from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import date
from django.core.exceptions import ValidationError
from .models import Device


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Abschicken"))

    class Meta:
        model = Device
        fields = (
            "manufacturer",
            "name",
            "model",
            "description",
            "serial_number",
            "buyed_at",
            "guarantee_end",
            "proof_of_purchase",
            "manual",
            "image",
        )

        widgets = {
            "guarantee_end": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date"}
            ),
            "buyed_at": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date"}
            )
        }

    def clean(self) -> dict:
        """
        validierung von dates
        """
        super().clean()
        buyed_at = self.cleaned_data.get("buyed_at")
        guarantee_end = self.cleaned_data.get("guarantee_end")

        if isinstance(buyed_at, date) and isinstance(guarantee_end, date):
            if guarantee_end < buyed_at:
                self._errors["guarantee_end"] = self.error_class(
                    ["Das Ende der Garantie kann nicht vor dem Kaufdatum liegen"]
                )
                raise ValidationError("Das Ende der Garantie kann nicht vor dem Kaufdatum liegen")

        return self.cleaned_data
