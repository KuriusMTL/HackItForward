from app.forms import ProfileUpdateForm
from app.models import Challenge, Profile, Project, SocialLinkAttachement, Tag

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import get_object_or_404, redirect


class IndexView(TemplateView):
    template_name = "explore.html"

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("type") not in ["challenge", "project", None]:
            return redirect("index")
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tags"] = Tag.objects.all()

        if "type" not in self.request.GET or (
            "q" not in self.request.GET and "tag" not in self.request.GET
        ):
            context["objects"] = {
                "challenge": Challenge.objects.all()[:3],
                "project": Project.objects.all()[:9],
            }
            return context

        initiative = self.request.GET["type"]
        if initiative == "challenge":
            queryset = Challenge.objects.all()
        elif initiative == "project":
            queryset = Project.objects.all()

        context["selected_tags"] = Tag.objects.filter(name__in=self.request.GET.getlist("tag"))
        for tag in context["selected_tags"]:
            queryset = queryset.filter(tags__in=[tag])

        search = context["q"] = self.request.GET.get("q", "")
        queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

        context["objects"] = {initiative: queryset.distinct()}
        return context


class UserView(DetailView):
    template_name = "userhome.html"
    model = Profile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = (
            Project.objects.filter(
                Q(creators__in=[self.object.pk]) | Q(contributors__in=[self.object.pk])
            )
            .distinct()
            .order_by("-created")
        )
        context["links"] = SocialLinkAttachement.objects.filter(
            object_id=self.object.pk,
            content_type=ContentType.objects.get_for_model(Profile),
        )
        return context


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
        return super().form_valid(form)


class InitiativeMixin(ContextMixin):
    classname = None
    initiative = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        self.initiative = self.classname.objects.get(pk=pk)

        context["initiative"] = self.initiative
        context["links"] = SocialLinkAttachement.objects.filter(
            object_id=pk, content_type=ContentType.objects.get_for_model(self.classname)
        )
        return context


class ChallengeView(InitiativeMixin, TemplateView):
    template_name = "challenge.html"
    classname = Challenge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_labels"] = [
            {"label": "Start Time", "time": self.initiative.start},
            {"label": "End Time", "time": self.initiative.end},
        ]
        context["projects"] = Project.objects.filter(challenge=self.initiative)
        return context


class ProjectView(InitiativeMixin, TemplateView):
    template_name = "project.html"
    classname = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_labels"] = [{"label": "Creation Time", "time": self.initiative.created}]
        return context
