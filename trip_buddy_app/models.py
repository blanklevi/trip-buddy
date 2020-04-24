from django.db import models
import re
import datetime
from django.core.exceptions import ValidationError


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        FN_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not FN_REGEX.match(postData['first_name']):
            errors['first_name'] = "Only letters can be used in the Name field!"
        LN_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not LN_REGEX.match(postData['last_name']):
            errors['last_name'] = "Only letters can be used in this field!"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        PW_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')
        if not PW_REGEX.match(postData['password']):
            errors['password'] = "Invalid characters!"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long!"
        if len(postData['email']) < 2:
            errors['email'] = "Email address is required!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long!"
        return errors

    def log_in_validator(self, postData):
        errors = {}
        if len(postData['log_email']) < 2:
            errors['log_email'] = "Email address is required!"
        if len(postData['log_pw']) < 8:
            errors['log_pw'] = "Password must be at least 8 characters long!"
        return errors


class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 2:
            errors['destination'] = "A destination must be provided!"
        if len(postData['start_date']) < 1:
            errors['start_date'] = "A start date must be provided!"
        if len(postData['end_date']) < 1:
            errors['end_date'] = "An end date must be provided!"
        if len(postData['plan']) < 2:
            errors['plan'] = "A plan must be provided!"
        return errors

    def edit_trip_validator(self, postData):
        errors = {}
        if len(postData['edit_destination']) < 2:
            errors['edit_destination'] = "A destination must be provided!"
        if len(postData['edit_start_date']) < 1:
            errors['edit_start_date'] = "A start date must be provided!"
        if len(postData['edit_end_date']) < 1:
            errors['edit_end_date'] = "An end date must be provided!"
        if len(postData['edit_plan']) < 2:
            errors['edit_plan'] = "A plan must be provided!"
        if postData['edit_start_date'] < str(datetime.date.today()):
            errors['edit_start_date'] = "The date cannot be in the past"
        if postData['edit_end_date'] < str(datetime.date.today()):
            errors['edit_end_date'] = "The date cannot be in the past"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Trip(models.Model):
    users = models.ManyToManyField(User, related_name="trips")
    destination = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
