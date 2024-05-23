import uuid
from django.contrib.auth.models import User
from django.db import models


class UserProfile(User):
    access_key = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Test(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Questions(models.Model):
    question = models.TextField(null=True, blank=True)
    variants = models.JSONField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Result(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    variants = models.JSONField(null=True, blank=True)
    max_answers = models.IntegerField(null=True, blank=True)
    correct_answers = models.IntegerField(null=True, blank=True)


class ActiveTest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    variants = models.JSONField(null=True, blank=True)
