from app.models import Profile

def profile(request):
    if not request.user.is_authenticated:
        return {}
    return {"profile": request.user.profile}
