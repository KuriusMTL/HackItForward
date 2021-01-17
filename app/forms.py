from app.models import Profile, Tag, SocialLinkAttachement

from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator, URLValidator, validate_email
from django.db import models
from django.forms import modelformset_factory, HiddenInput, ValidationError
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.html import escape


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["description", "tags"]
        hidden_fields = ["longitude", "latitude"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["tags"].widget = CheckboxSelectMultiple()
        self.fields["tags"].queryset = Tag.objects.all()


class SocialLinkForm(ModelForm):
    class Meta:
        model = SocialLinkAttachement
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        if "obj" in kwargs:
            self.object = kwargs.pop("obj")

        super(SocialLinkForm, self).__init__(*args, **kwargs)
        self.fields["content_type"].widget = HiddenInput()
        self.fields["object_id"].widget = HiddenInput()
        self.fields["content_type"].disabled = True
        self.fields["object_id"].disabled = True


    def clean_object_id(self):
        cleaned_data = self.cleaned_data
        if hasattr(self, "object"):
            cleaned_data["object_id"] = self.object.pk
        return cleaned_data["object_id"]

    def clean_content_type(self):
        cleaned_data = self.cleaned_data
        cleaned_data["content_type"] = ContentType.objects.get_for_model(self.object.__class__)
        return cleaned_data["content_type"]

    def clean_content(self):
        data = self.cleaned_data["content"]
        if data.lower().startswith("mailto:"):
            validate_email(data[7:])
        elif data.lower().startswith("tel:"):
            validate_tel = RegexValidator(r"^[0-9]+$", "Enter a valid telephone number")
            validate_tel(data[4:])
        else:
            validate_url = URLValidator()
            validate_url(data)
        data = escape(data)
        return data


SocialLinkFormSet = modelformset_factory(
    SocialLinkAttachement,
    form=SocialLinkForm,
    exclude=("id",),
    extra=0,
    can_delete=True,
)
