from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "individual-polling-unit",
        views.IndividualPollUnitView.as_view(),
        name="individual-polling-unit",
    ),
    path(
        "summed-polling-units-in-lga",
        views.SummedPollUnitsInLgaView.as_view(),
        name="summed-polling-units-in-lga",
    ),
    path(
        "store-new-polling-unit-result",
        views.StoreNewPollingUnitResultView.as_view(),
        name="store-new-polling-unit-result",
    ),
]
