from app.models import Profile, Tag

from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from app.countries_data import countries


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description", "tags", "country"]
        hidden_fields = ["longitude", "latitude"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()

    def clean(self):
        self.hidden_feild["longitude"] = countries[self.feilds["country"]]["Longitude"]
        self.hidden_feild["latitude"] = countries[self.feilds["country"]]["Latitude"]