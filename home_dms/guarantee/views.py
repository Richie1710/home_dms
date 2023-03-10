from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q, QuerySet
from .models import Device
from .forms import DeviceForm


class DeviceListView(ListView):
    """
    Listing of all Devices
    """

    paginate_by = 20
    model = Device
    queryset = Device.objects.order_by("pk").all()


class DeviceDetailView(DetailView):
    """
    Show details for Device
    """

    model = Device


class DeviceDeleteView(SuccessMessageMixin, DeleteView):
    """
    Delete Device
    """

    model = Device
    success_url = reverse_lazy("guarantee:guarantee_list")
    success_message = "Objekt erfolgreich gelöscht"


class DeviceCreateView(SuccessMessageMixin, CreateView):
    """
    Create New Device
    """

    model = Device
    form_class = DeviceForm
    success_message = "Das Gerät wurde erfolgreich registriert"


class DeviceUpdateView(SuccessMessageMixin, UpdateView):
    """
    Update Device Info
    """

    model = Device
    form_class = DeviceForm
    success_message = "Die Infos zum Gerät wurden erfolgreich geupdated"


class DeviceSearchView(ListView):
    """
    Search for Device
    """

    model = Device

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        q = self.request.GET.get("q", "")
        return qs.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(manufacturer__icontains=q)
            | Q(model__icontains=q)
        )
