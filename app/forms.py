from app.models import Profile, Tag, SocialLinkAttachement

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import modelformset_factory, HiddenInput, ValidationError
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple


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

        if getattr(self, "object", None) is not None:
            self.fields["content_type"].initial = ContentType.objects.get_for_model(
                self.object.__class__
            )

    def clean_object_id(self):
        cleaned_data = self.cleaned_data
        if getattr(self, "object", None) is not None:
            cleaned_data["object_id"] = self.object.pk
        elif self.fields["object_id"].initial is not None:
            cleaned_data["object_id"] = self.fields["object_id"].initial
        return cleaned_data["object_id"]

    def clean_content_type(self):
        cleaned_data = self.cleaned_data
        if (
            "content_type" not in cleaned_data
            or cleaned_data["content_type"] != self.fields["content_type"].initial
        ):
            raise ValidationError("content_type should not be modified")
        return cleaned_data["content_type"]


SocialLinkFormSet = modelformset_factory(
    SocialLinkAttachement,
    form=SocialLinkForm,
    exclude=("id",),
    extra=0,
    can_delete=True,
)
