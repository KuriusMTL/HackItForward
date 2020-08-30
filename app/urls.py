from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("home/", views.UserView.as_view(), name="home"),
    path("home/<int:pk>", views.UserView.as_view(), name="user"),
    path("profile/edit", views.EditProfileView.as_view(), name="edit_profile"),
    path("challenge/<int:pk>/", views.ChallengeView.as_view(), name="challenge"),
    path("project/<int:pk>/", views.ProjectView.as_view(), name="project"),
]
