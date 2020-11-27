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


class SocialLink(models.Model):
    name = models.CharField(
        max_length=24, verbose_name="Name", help_text="Name of this social link."
    )
    icon = models.CharField(
        max_length=32, verbose_name="Icon", help_text="CSS FA icon class without 'fa-' prefix."
    )
    site = models.CharField(
        max_length=2047,
        verbose_name="Site",
        help_text="Python format string which will have '%s' replaced with the link content.",
    )
    placeholder = models.CharField(
        max_length=32,
        verbose_name="Placeholder",
        help_text="Placeholder text displayed to the user when creating a link.",
    )

    def __str__(self):
        return self.name


class SocialLinkAttachement(models.Model):
    link = models.ForeignKey(
        SocialLink,
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name="Link",
        help_text="Social link of this link attachment.",
    )
    content = models.CharField(
        max_length=2047,
        verbose_name="Content",
        help_text="URL or username to be replaced in social link.",
    )
    content_type = models.ForeignKey(
        ContentType, verbose_name="Linked Item Type", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(verbose_name="Linked Item ID")
    linked_item = GenericForeignKey()

    @property
    def href(self):
        return self.link.site % self.content

    def __str__(self):
        return self.href


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
