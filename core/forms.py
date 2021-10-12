from django import forms

from .fields import GroupedModelChoiceField
from .models import Agentname, Lga, Party, PollingUnit, States


class GetPollingUnitDataForm(forms.Form):
    available_lgas = Lga.objects.filter(state_id="25").values_list("lga_id", flat=True)

    polling_unit = GroupedModelChoiceField(
        label="Polling Unit Number",
        help_text="Choose a polling unit based on the polling unit number.",
        queryset=PollingUnit.objects.filter(lga_id__in=available_lgas),
        choices_groupby=lambda obj: Lga.objects.get(lga_id=obj.lga_id).lga_name,
    )


class GetSummedPollingUnitsResultsinLgaForm(forms.Form):
    lga = GroupedModelChoiceField(
        label="Local Government Area",
        queryset=Lga.objects.all(),
        choices_groupby=lambda obj: States.objects.get(state_id=obj.state_id).state_name,
        help_text="Select a local government area.",
    )


class StoreNewPollingUnitResultForm(forms.Form):
    available_lgas = Lga.objects.filter(state_id="25").values_list("lga_id", flat=True)

    party = forms.ModelChoiceField(label="Party", queryset=Party.objects.all())
    party_score = forms.IntegerField(label="Party Score")
    polling_unit = GroupedModelChoiceField(
        label="Polling Unit",
        help_text="Choose a polling unit based on the polling unit number.",
        queryset=PollingUnit.objects.filter(lga_id__in=available_lgas),
        choices_groupby=lambda obj: Lga.objects.get(lga_id=obj.lga_id).lga_name,
    )
    entered_by_user = forms.ModelChoiceField(
        label="Agent",
        queryset=Agentname.objects.all(),
        help_text="The name of the agent uploading the data.",
    )
