"""models."""

from django.db import models


class TimeStampedModel(models.Model):
    """Time stamped model."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Color(TimeStampedModel):
    """Color model."""

    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name


class Person(TimeStampedModel):
    """Person model."""

    name = models.CharField(max_length=200)
    age = models.IntegerField()
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, related_name="person_color"
    )

    def __str__(self):
        return self.name
