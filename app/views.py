from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

class IndexView(TemplateView):
    template_name = "index.html"


class HomeView(TemplateView):
    template_name = "userhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile"] = self.request.user.profile
        return context

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("/profile/edit")

    def form_valid(self, form):
        form.save()
        login(self.request, form.instance)
        Profile.objects.create(user=form.instance)
        return super().form_valid(form)
