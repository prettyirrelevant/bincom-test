from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils import timezone
from django.views import generic

from .forms import (GetPollingUnitDataForm,
                    GetSummedPollingUnitsResultsinLgaForm,
                    StoreNewPollingUnitResultForm)
from .models import AnnouncedPuResults, PollingUnit
from .utils import aggregrate_party_and_score


class IndividualPollUnitView(generic.FormView):
    template_name = "individual_polling_unit.html"
    form_class = GetPollingUnitDataForm
    success_url = reverse_lazy("core:individual-polling-unit")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Individual Polling Units | Bincom Django Test"

        return context

    def form_valid(self, form):
        polling_unit = form.cleaned_data.get("polling_unit")
        polling_unit_number = polling_unit.polling_unit_number

        # store result in session to display.
        uniqueid = PollingUnit.objects.get(polling_unit_number=polling_unit_number).uniqueid

        self.request.session["individual_results"] = AnnouncedPuResults.get_results(uniqueid)
        self.request.session["polling_unit_number"] = polling_unit_number
        self.request.session["polling_unit_name"] = polling_unit.polling_unit_name

        return redirect(self.get_success_url())


class SummedPollUnitsInLgaView(generic.FormView):
    template_name = "summed_pu_in_lga.html"
    form_class = GetSummedPollingUnitsResultsinLgaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Summed Polling Units in LGA | Bincom Django Test"

        return context

    def form_valid(self, form):
        lga_id = form.cleaned_data.get("lga").lga_id
        lga_name = form.cleaned_data.get("lga").lga_name

        all_polling_units = list(
            PollingUnit.objects.filter(lga_id=lga_id).values_list("uniqueid", flat=True)
        )
        results_for_polling_units = AnnouncedPuResults.objects.filter(
            polling_unit_uniqueid__in=all_polling_units
        )
        pu_results_for_lga = aggregrate_party_and_score(
            results_for_polling_units.values(
                "party_abbreviation", "party_score", "entered_by_user"
            )
        )
        self.request.session["lga_results"] = pu_results_for_lga
        self.request.session["lga_name"] = lga_name

        return redirect(reverse("core:summed-polling-units-in-lga"))


class StoreNewPollingUnitResultView(generic.FormView):
    template_name = "store_new_polling_unit_result.html"
    form_class = StoreNewPollingUnitResultForm
    success_url = reverse_lazy("core:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Store New Polling Unit Result | Bincom Django Test"

        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        polling_unit_uniqueid = form.cleaned_data.pop("polling_unit").uniqueid
        party_abbr = form.cleaned_data.pop("party").partyname

        cleaned_data.update(
            {
                "polling_unit_uniqueid": polling_unit_uniqueid,
                "party_abbreviation": party_abbr,
            }
        )

        _, created = AnnouncedPuResults.objects.get_or_create(
            **cleaned_data,
            defaults={"date_entered": timezone.now(), "user_ip_address": "192.168.0.1"}
        )

        if created:
            messages.success(self.request, "New polling result stored successfully!")
            return redirect(self.get_success_url())

        messages.error(self.request, "The data you are trying to save already exists!")
        return redirect(reverse("core:store-new-polling-unit-result"))


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Bincom Django Test"

        return context
