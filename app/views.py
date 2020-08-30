from app.models import Challenge, Project

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


class IndexView(TemplateView):
    template_name = "explore.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["challenges"] = Challenge.objects.all()[:3]
        context["projects"] = Project.objects.all()[:9]
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "userhome.html"
    login_url = reverse_lazy("home")



class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("edit_profile")

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        Profile.objects.create(user=form.instance)
        return super().form_valid(form)
