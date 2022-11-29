from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# Create your models here.
class Config(models.Model):
    class Meta:
        verbose_name = "Devote Frontend"

class Voters(models.Model):
    name = models.CharField(max_length=64, verbose_name="Name")
    username = models.CharField(max_length=64, verbose_name="Username")
    identifier = models.CharField(max_length=16, verbose_name="Unique Identifier")
    block = models.TextField(max_length=64, verbose_name="Block content")
    timestamp = models.TimeField(auto_now_add=True, null=True, verbose_name="Timestamp")

    def __str__(self):
        return 'Vote by: ' + self.name

    def clean(self):
        if len(self.block_content) != 64:
            raise ValidationError("Error hashing block")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"