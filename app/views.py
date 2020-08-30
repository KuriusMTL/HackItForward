from app.forms import ProfileUpdateForm
from app.models import Challenge, Profile, Project, SocialLinkAttachement, Task

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView

from django.contrib.contenttypes.models import ContentType


class IndexView(TemplateView):
    template_name = "explore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "type" not in self.request.GET or "q" not in self.request.GET:
            context["challenges"] = Challenge.objects.all()[:3]
            context["projects"] = Project.objects.all()[:9]
            return context
        query = self.request.GET["q"]
        if self.request.GET["type"] == "challenge":
            context["challenges"] = Challenge.objects.all().filter(
                Q(name__contains=query) | Q(description__contains=query)
            )
        elif self.request.GET["type"] == "project":
            context["projects"] = Project.objects.all().filter(
                Q(name__contains=query) | Q(description__contains=query)
            )
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "userhome.html"
    login_url = reverse_lazy("home")


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = "edit_profile.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("edit_profile")

    def get_object(self, queryset=None):
        return self.request.user.profile


class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("edit_profile")

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        Profile.objects.create(user=form.instance)
        return super().form_valid(form)


class ChallengeView(TemplateView):
    template_name = "challenge.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        challenge = Challenge.objects.get(pk=pk)
        context["initiative"] = challenge
        context["projects"] = Project.objects.filter(challenge=challenge)
        context["links"] = SocialLinkAttachement.objects.filter(
            object_id=pk, content_type=ContentType.objects.get_for_model(Challenge)
        )
        context["time_labels"] = [
            {"label": "Start Time", "time": challenge.start},
            {"label": "End Time", "time": challenge.end},
        ]
        return context


class ProjectView(TemplateView):
    template_name = "project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        project = Project.objects.get(pk=pk)
        context["initiative"] = project
        context["tasks"] = Task.objects.filter(project=project)
        context["links"] = SocialLinkAttachement.objects.filter(
            object_id=pk, content_type=ContentType.objects.get_for_model(Project)
        )
        context["time_labels"] = [{"label": "Creation Time", "time": project.created}]
        return context
