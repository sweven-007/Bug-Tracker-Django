from django.db import models
from django.db.models import CharField, DateTimeField, EmailField, IntegerField, TextField, ForeignKey, ImageField, BooleanField
from datetime import datetime


class Admin(models.Model):
    name = CharField(max_length=100)
    email = EmailField(max_length=255)
    password = CharField(max_length=100)
    date_of_join = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} [{self.date_of_join}]"


class User(models.Model):
    name = CharField(max_length=100)
    email = EmailField(max_length=255)
    password = CharField(max_length=100)
    date_of_join = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} [{self.date_of_join}]"


class Developer(models.Model):
    name = CharField(max_length=100)
    email = EmailField(max_length=255)
    password = CharField(max_length=100)
    date_of_join = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} [{self.date_of_join}]"


class Priority(models.Model):
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Bug(models.Model):
    bug_id = models.AutoField(primary_key=True)
    name = CharField(max_length=150)
    description = TextField()
    priority = ForeignKey('Priority', on_delete=models.CASCADE)
    category = ForeignKey('Category', on_delete=models.CASCADE)
    screenshot = ImageField(upload_to='screenshots/', blank=True, null=True)
    assigned_to = ForeignKey(
        'Developer', on_delete=models.CASCADE, null=True, blank=True)
    assigned_by = ForeignKey(
        'Admin', on_delete=models.CASCADE, null=True, blank=True)
    raised_by = ForeignKey('User', on_delete=models.CASCADE)
    timestamp = DateTimeField(default=datetime.now)
    resolved = BooleanField(default=False)
    rejected = BooleanField(default=False)

    def __str__(self):
        return f"{self.bug_id}. {self.name} <- {self.raised_by} [{self.timestamp}]"
