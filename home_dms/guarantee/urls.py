from django.urls import path
from . import views


app_name = "guarantee"

urlpatterns = [
    path("", views.DeviceListView.as_view(), name="guarantee_list"),
    path("guarantee/add", views.DeviceCreateView.as_view(),
         name="guarantee_add"),
    path(
        "guarantee/<int:pk>", views.DeviceDetailView.as_view(),
        name="guarantee_detail"
    ),
    path(
        "guarantee/<int:pk>/delete",
        views.DeviceDeleteView.as_view(),
        name="guarantee_delete",
    ),
    path(
        "guarantee/<int:pk>/edit",
        views.DeviceUpdateView.as_view(),
        name="guarantee_update",
    ),
    path(
        "guarantee/search",
        views.DeviceSearchView.as_view(),
        name="guarantee_search"
    )
    ]
