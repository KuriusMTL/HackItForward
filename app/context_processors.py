from app.models import Profile


def profile(request):
    if not request.user.is_authenticated:
        return {}
    profile = Profile.objects.get_or_create(user=request.user)[0]
    return {"profile": profile}
