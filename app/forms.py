from app.models import Profile, Tag, SocialLinkAttachement, User

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import modelformset_factory, HiddenInput, ValidationError
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request") # it's best you pop request, so that you don't get any complains for a parent that checks what kwargs it gets
        super(PasswordUpdateForm, self).__init__(request.user)



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "banner_image","location", "description", "tags"]
        hidden_fields = ["longitude", "latitude"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
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
        self.fields["object_id"].disabled = True
        self.fields["content_type"].disabled = True

    def clean_object_id(self):
        cleaned_data = self.cleaned_data
        if hasattr(self, "object"):
            cleaned_data["object_id"] = self.object.pk
        return cleaned_data["object_id"]

    def clean_content_type(self):
        cleaned_data = self.cleaned_data
        cleaned_data["content_type"] = ContentType.objects.get_for_model(self.object.__class__)
        return cleaned_data["content_type"]


SocialLinkFormSet = modelformset_factory(
    SocialLinkAttachement,
    form=SocialLinkForm,
    exclude=("id",),
    extra=0,
    can_delete=True,
)
