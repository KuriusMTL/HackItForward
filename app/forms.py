from app.models import Profile, Tag

from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from app.countries_data import countries


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description", "tags", "country","longitude", "latitude"]

        def clean(self):
            print("lookin good")
            self.fields["longitude"] = countries[self.fields["country"]]["Longitude"]
            self.fields["latitude"] = countries[self.fields["country"]]["Latitude"]
            print(self.fields["longitude"])
            print(self.fields["latitude"])


    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()

    