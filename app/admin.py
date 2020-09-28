from django.contrib import admin
from app.models import (
    SocialLink,
    SocialLinkAttachement,
    Badge,
    Tag,
    Profile,
    Challenge,
    Project,
    Notification,
    NotificationInstance,
)

admin.site.register(SocialLink)
admin.site.register(SocialLinkAttachement)
admin.site.register(Badge)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Challenge)
admin.site.register(Project)
admin.site.register(Notification)
admin.site.register(NotificationInstance)
