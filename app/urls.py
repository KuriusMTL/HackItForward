from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("explore/", views.ExploreView.as_view(), name="explore"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("login/social/", include("social_django.urls", namespace="social")),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    # TODO: Rename this to fit in line with project and challenge style.
    path("profile/", views.UserView.as_view(), name="profile"),
    path("profile/<int:pk>", views.UserView.as_view(), name="user"),
    path("profile/edit", views.EditProfileView.as_view(), name="edit_profile"),
    path("challenge/create/", views.ChallengeCreateView.as_view(), name="challenge_create"),
    path("challenge/<int:pk>/", views.ChallengeView.as_view(), name="challenge"),
    path("challenge/<int:pk>/edit/", views.ChallengeUpdateView.as_view(), name="challenge_edit"),
    path("project/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "project/create/<int:pk>/",
        views.ProjectChallengeCreateView.as_view(),
        name="project_challenge_create",
    ),
    path("project/<int:pk>/", views.ProjectView.as_view(), name="project"),
    path("project/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_edit"),
]
