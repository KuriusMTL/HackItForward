from app.forms import ProfileUpdateForm
from app.models import Challenge, Profile, Project, SocialLinkAttachement, Tag

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.forms.widgets import CheckboxSelectMultiple
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import FormView, UpdateView

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


class IndexView(TemplateView):
    template_name = "explore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tags"] = Tag.objects.all()
        context["selected_tags"] = []

        if "type" not in self.request.GET or (
            "q" not in self.request.GET and "tag" not in self.request.GET
        ):
            context["objects"] = {
                "challenge": Challenge.objects.all()[:3],
                "project": Project.objects.all()[:9],
            }
        else:
            initiative = self.request.GET["type"]

            if initiative == "challenge":
                queryset = Challenge.objects.all()
            elif initiative == "project":
                queryset = Project.objects.all()

            if "tag" in self.request.GET:
                query = self.request.GET.getlist("tag")

                for tag in query:
                    currtags = Tag.objects.filter(name__iexact=tag)
                    queryset = queryset.filter(Q(tags__in=currtags))
                    context["selected_tags"] += currtags

            if "q" in self.request.GET:
                query = self.request.GET["q"]
                context["q"] = query

                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                )

            context["objects"] = {initiative: queryset.distinct()}

        return context


# TODO: Change to DetailView
class UserView(UserPassesTestMixin, TemplateView):
    template_name = "userhome.html"

    def test_func(self):
        return not self.request.user.is_anonymous or "pk" in self.kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.profile.pk if "pk" not in self.kwargs else self.kwargs["pk"]

        profile = get_object_or_404(Profile, pk=pk)
        context["profile"] = profile
        context["projects"] = (
            Project.objects.filter(Q(creators__in=[profile]) | Q(contributors__in=[profile]))
            .distinct()
            .order_by("-created")
        )
        context["links"] = SocialLinkAttachement.objects.filter(
            object_id=pk,
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
        Profile.objects.create(user=form.instance)
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
