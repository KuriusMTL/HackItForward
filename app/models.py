from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SocialLink(models.Model):
    name = models.CharField(
        max_length=24, verbose_name="Name", help_text="Name of this social link."
    )
    icon = models.CharField(
        max_length=32, verbose_name="Icon", help_text="CSS ZMDI icon class without 'zmdi-' prefix."
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
    CATEGORY_CHOICES = [
        ("S", "Skill"),
        ("L", "Location"),
        ("K", "Knowledge"),
        ("I", "Importance"),
    ]

    name = models.CharField(max_length=24, verbose_name="Name", help_text="Name of this tag.")
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        verbose_name="Category",
        help_text="Category of this tag which determines where it is available and presented.",
    )
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
        blank=True, verbose_name="Description", help_text="Description of this challenge."
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="challenges",
        verbose_name="Tags",
        help_text="Tags associated with this challenge.",
    )
    creators = models.ManyToManyField(
        User,
        related_name="created_challenges",
        verbose_name="Creators",
        help_text="Creators of this challenge which can edit its properties.",
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name="Creation Date",
        help_text="Date this challenge was created.",
    )
    start = models.DateTimeField(
        blank=True,
        verbose_name="Challenge Start",
        help_text="Start date and time when projects can be created for this challenge.",
    )
    end = models.DateTimeField(
        blank=True,
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
        upload_to="challenges/", verbose_name="Image", help_text="Cover image of this challenge."
    )

    @property
    def short_creators(self):
        if self.creators.count() == 1:
            return self.creators.first().username
        return "%s, et al." % self.creators.first().username

    def __str__(self):
        return self.name


class Project(models.Model):
    challenge = models.ForeignKey(Challenge, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, verbose_name="Name", help_text="Name of this project.")
    description = models.TextField(
        blank=True, verbose_name="Description", help_text="Description of this project."
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="projects",
        verbose_name="Tags",
        help_text="Tags associated with this project.",
    )
    contributors = models.ManyToManyField(
        Profile,
        blank=True,
        related_name="contributed_projects",
        verbose_name="Contributors",
        help_text="Those who have completed tasks for this project.",
    )
    creators = models.ManyToManyField(
        Profile,
        related_name="created_projects",
        verbose_name="Creators",
        help_text="Creators of this project which can edit its properties.",
    )
    created = models.DateField(
        auto_now_add=True, verbose_name="Creation Date", help_text="Date this project was created."
    )
    image = models.ImageField(
        upload_to="challenges/", verbose_name="Image", help_text="Cover image of this project."
    )

    @property
    def short_creators(self):
        if self.creators.count() == 1:
            return self.creators.first().username
        return "%s, et al." % self.creators.first().username

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", null=True, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ("T", "TODO"),
        ("I", "In-Progress"),
        ("C", "Completed"),
    ]

    name = models.CharField(max_length=100, verbose_name="Name", help_text="Name of this task.")
    description = models.TextField(
        blank=True, verbose_name="Description", help_text="Description of this task."
    )
    status = models.CharField(max_length=1, verbose_name="Status", help_text="Status of this task.")
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tags",
        verbose_name="Tags",
        help_text="Tags associated with this task.",
    )

    def __str__(self):
        return self.name


class TaskSubmission(models.Model):
    STATUS_CHOICES = [
        ("P", "Pending"),
        ("C", "Requested Changes"),
        ("R", "Rejected"),
        ("A", "Accepted"),
    ]

    task = models.ForeignKey(Task, related_name="submissions", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name="submissions", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, verbose_name="Status", help_text="Status of this submission."
    )
    description = models.TextField(
        blank=True, verbose_name="Description", help_text="Description of this submission."
    )

    def __str__(self):
        return "'%s' submission by '%s'" % (self.task.name, self.user.username)
