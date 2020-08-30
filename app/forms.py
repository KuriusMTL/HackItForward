from app.models import Profile, Tag

from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description", "tags"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all().filter(category="K")
