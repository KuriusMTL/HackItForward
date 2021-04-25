from django.contrib import admin
from app.models import (
    SocialLinkAttachement,
    Badge,
    Tag,
    Profile,
    Challenge,
    Project,
    Comment
)

admin.site.register(SocialLinkAttachement)
admin.site.register(Badge)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Challenge)
admin.site.register(Project)
admin.site.register(Comment)