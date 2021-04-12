from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("explore/", views.IndexView.as_view(), name="explore"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("gallery/", views.GalleryView.as_view(), name="gallery"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("onboarding/", views.OnboardingView.as_view(), name="onboarding"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("login/social/", include("social_django.urls", namespace="social")),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    # TODO: Rename this to fit in line with project and challenge style.
    path("profile/", views.UserView.as_view(), name="profile"),
    # Enables to visit any user's profile by inserting their username
    path("profile/<str:username>", views.UserView.as_view(), name="user"),
    path("edit/profile", views.EditProfileView.as_view(), name="edit_profile"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'), name="password_change"),
    path("password_change_confirmation/",
         views.PasswordChangeConfirmationView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name="password_reset"),
    path("password_reset_confirmation/",
         views.PasswordResetConfirmationView.as_view(), name="password_reset_done"),
    path("challenge/create/", views.ChallengeCreateView.as_view(),
         name="challenge_create"),
    path("challenge/<int:pk>/", views.ChallengeView.as_view(), name="challenge"),
    path("challenge/<int:pk>/edit/",
         views.ChallengeUpdateView.as_view(), name="challenge_edit"),
    path("project/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path(
        "project/create/<int:pk>/",
        views.ProjectChallengeCreateView.as_view(),
        name="project_challenge_create",
    ),
    path("project/<int:pk>/", views.ProjectView.as_view(), name="project"),
    path("project/<int:pk>/edit/",
         views.ProjectUpdateView.as_view(), name="project_edit"),
    path("get_challenges_ajax/", views.get_challenges_ajax,
         name="get_challenges_ajax"),
]
