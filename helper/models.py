from django.db import models


class UserData(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class NotesData(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

