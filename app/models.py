from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import re


PROJECT_DESCRIPTION = """
# Project Name

A longer description of the project compared to the one liner.

## Features

Talk about some cool things your project does here. You can use a:
 - Bulleted
 - List
 - Like
 - This

## Installation

You should explain how to install the project in this section.
 1. Numbered
 2. Lists
 3. Are
 4. Useful
"""

CHALLENGE_DESCRIPTION = """
# Challenge Name

A longer description of the project compared to the one liner.

## Tasks

Provide a simple, bulleted list of tasks that you would like project creators to accomplish:
 - Task 1
 - Task 2
 - Task 3

## Extra Resources

If there are extra tools that you think project makers could benefit them, include them here.
"""

"""
# FORMAT
name: "Name of this social link"
icon: "CSS FA icon class without 'fa-' prefix"
regex: "regular expression to match this link"
fa: "Font Awesome CSS class to use" (optional; defaults to "fab")
"""
SOCIAL_LINKS = [
    {"name": "Twitter", "icon": "twitter", "regex": r"(^(https?:\/\/)?)twitter\.com\/.*"},
    {"name": "Facebook", "icon": "facebook", "regex": r"(^(https?:\/\/)?)facebook\.com\/.*"},
    {"name": "Github", "icon": "github", "regex": r"(^(https?:\/\/)?)github\.com\/.*"},
    {"name": "Reddit", "icon": "reddit", "regex": r"(^(https?:\/\/)?)reddit\.com\/.*"},
    {"name": "Steam", "icon": "steam", "regex": r"(^(https?:\/\/)?)steamcommunity\.com\/.*"},
    {"name": "YouTube", "icon": "youtube", "regex": r"(^(https?:\/\/)?)youtube\.com\/.*"},
    {
        "name": "Stack Overflow",
        "icon": "stack-overflow",
        "regex": r"(^(https?:\/\/)?)stackoverflow\.com\/.*",
    },
    {"name": "Vimeo", "icon": "vimeo-v", "regex": r"(^(https?:\/\/)?)vimeo\.com\/.*"},
    {"name": "SoundCloud", "icon": "soundcloud", "regex": r"(^(https?:\/\/)?)soundcloud\.com\/.*"},
    {"name": "Instagram", "icon": "instagram", "regex": r"(^(https?:\/\/)?)instagram\.com\/.*"},
    {
        "name": "Email",
        "icon": "envelope",
        "fa": "fas",
        "regex": r"^mailto:(.+@[a-z0-9\.-]+)$",
    },
    {"name": "Phone Number", "icon": "phone", "fa": "fas", "regex": r"^tel:[0-9]+$"},
]


class SocialLinkAttachement(models.Model):
    content = models.CharField(
        max_length=2047,
        verbose_name="Link",
        help_text="The actual link.",
    )
    content_type = models.ForeignKey(
        ContentType, verbose_name="Linked Item Type", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(verbose_name="Linked Item ID")
    linked_item = GenericForeignKey()

    def social_link(self):
        for link in SOCIAL_LINKS:
            regex = re.compile(link["regex"], re.I)
            if regex.match(self.content):
                return link
        return {"name": "Generic Link", "icon": "link", "fa": "fas"}

    def fa_class(self):
        return self.social_link.get("fa", "fab")

    @property
    def icon(self):
        return self.social_link()["icon"]

    @property
    def name(self):
        return self.social_link()["name"]

    @property
    def css_class(self):
        return "%s fa-%s" % (self.fa_class(), self.icon)

    def __str__(self):
        return self.content


class Badge(models.Model):
    name = models.CharField(max_length=48, verbose_name="name", help_text="Name of this badge.")
    description = models.TextField(
        blank=True, verbose_name="Description", help_text="Description of this badge."
    )
    color = ColorField(help_text="Color", verbose_name="The color of this tag.")
    points = models.PositiveSmallIntegerField(
        verbose_name="Points", help_text="Points awarded for this badge."
    )
    icon = models.ImageField(upload_to="badges/", verbose_name="Image", help_text="Icon of badge.")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=24, verbose_name="Name", help_text="Name of this tag.")
    color = ColorField(help_text="Color", verbose_name="Color of this tag.")

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    description = models.TextField(
        blank=True, verbose_name="Description", help_text="User description."
    )
    badges = models.ManyToManyField(
        Badge,
        blank=True,
        related_name="profiles",
        verbose_name="Badges",
        help_text="Badges awarded to this user.",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="profiles",
        verbose_name="Tags",
        help_text="Tags associated with this user.",
    )

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class Challenge(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Name", help_text="Name of this challenge."
    )
    description = models.TextField(
        blank=True,
        default=CHALLENGE_DESCRIPTION,
        verbose_name="Description",
        help_text="Description of this challenge.",
    )
    one_liner = models.CharField(
        blank=True,
        verbose_name="One Liner",
        help_text="A one line description of this challenge.",
        max_length=50,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="challenges",
        verbose_name="Tags",
        help_text="Tags associated with this challenge.",
    )
    creators = models.ManyToManyField(
        Profile,
        related_name="created_challenges",
        verbose_name="Creators",
        help_text="Creators of this challenge which can edit its properties. Removing yourself "
        + "will make it impossible to edit this challenge.",
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name="Creation Date",
        help_text="Date this challenge was created.",
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Challenge Start",
        help_text="Start date and time when projects can be created for this challenge.",
    )
    end = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Challenge End",
        help_text="End date and time when projects can no longer be created for this challenge.",
    )
    rewards = models.ManyToManyField(
        Badge,
        blank=True,
        related_name="challenges",
        verbose_name="Rewards",
        help_text="Badges awareded to users that complete projects for this challenge.",
    )
    image = models.ImageField(
        blank=True,
        upload_to="challenges/",
        verbose_name="Image",
        help_text="Cover image of this challenge.",
    )

    def clean(self):
        if self.start and not self.end:
            raise ValidationError("An end date must be provided if you have a start date.")
        if not self.start and self.end:
            raise ValidationError("A start date must be provided if you have an end date.")
        if self.start and self.end and self.start >= self.end:
            raise ValidationError("The end date must be after the start date.")

    @property
    def short_creators(self):
        if self.creators.count() == 1:
            return self.creators.first().username
        return "%s, et al." % self.creators.first().username

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return self.creators.all().filter(id=user.profile.id).exists()

    def get_absolute_url(self):
        return reverse("challenge", args=[self.pk])

    def get_edit_url(self):
        return reverse("challenge_edit", args=[self.pk])

    def is_open(self):
        if not self.start or not self.end:
            return True
        return self.start <= timezone.now() <= self.end

    def __str__(self):
        return self.name


class Project(models.Model):
    challenge = models.ForeignKey(Challenge, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, verbose_name="Name", help_text="Name of this project.")
    description = models.TextField(
        blank=True,
        default=PROJECT_DESCRIPTION,
        verbose_name="Description",
        help_text="Description of this project.",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="projects",
        verbose_name="Tags",
        help_text="Tags associated with this project.",
    )
    one_liner = models.CharField(
        blank=True,
        verbose_name="One Liner",
        help_text="A one line description of this project.",
        max_length=50,
    )
    contributors = models.ManyToManyField(
        Profile,
        blank=True,
        related_name="contributed_projects",
        verbose_name="Contributors",
        help_text="Those who have contributed to this project.",
    )
    creators = models.ManyToManyField(
        Profile,
        related_name="created_projects",
        verbose_name="Creators",
        help_text="Creators of this project which can edit its properties. Removing yourself will "
        + "make it impossible for you to edit this project.",
    )
    created = models.DateField(
        auto_now_add=True, verbose_name="Creation Date", help_text="Date this project was created."
    )
    image = models.ImageField(
        blank=True,
        upload_to="challenges/",
        verbose_name="Image",
        help_text="Cover image of this project.",
    )

    @property
    def short_creators(self):
        if self.creators.count() == 1:
            return self.creators.first().username
        return "%s, et al." % self.creators.first().username

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return self.creators.all().filter(id=user.profile.id).exists()

    def get_absolute_url(self):
        return reverse("project", args=[self.pk])

    def get_edit_url(self):
        return reverse("project_edit", args=[self.pk])

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
