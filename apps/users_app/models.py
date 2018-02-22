# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Name Regular Expression
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

# Email Regular Expression
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Password Regular Expression
PW_REGEX = re.compile(r'^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$')

class UserManager(models.Manager):
    def login_validator(self, postData):
        password = postData['password']
        email = postData['email']

        errors = {}
        response = {
            'status': True,
            'info': {
                'email': postData['email']
            }
        }

        if len(response['info']) < 1:
            errors["login_email"] = "Email cannot be blank!"

        if len(password) < 1:
            errors["login_password"] = "Password cannot be blank!"

        if len(errors) == 0:
            exists = User.objects.filter(email = email)

            if len(exists):
                user=exists[0]
                hashed=user.password

                if bcrypt.hashpw(password.encode(), hashed.encode()) != hashed.encode():
                    errors["login_password"] = "Password does not match password on file."
                else:
                    response['user'] = user
            else:
                errors["login_email"] = "User doesn't exists! Use valid email address or register."

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors

        return response

    def registration_validator(self, postData):    
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        password = postData['password']
        confirm_pw = postData['confirm_pw']

        errors = {}
        response = {
            'status': True
        }

        if len(first_name) <= 0:
            errors["first_name"] = "First name cannot be blank!"
        elif len(first_name) >= 1 and len(first_name) < 2:
            errors["first_name"] = "First name must have 2 letters!"
        elif not NAME_REGEX.match(first_name):
            errors["first_name"] = "Name can only contain letters!"

        if len(last_name) <= 0:
            errors["last_name"] = "Last name cannot be blank!"
        elif len(last_name) >= 1 and len(last_name) < 2:
            errors["last_name"] = "Last name must have 2 letters!"
        elif not NAME_REGEX.match(last_name):
            errors["last_name"] = "Name can only contain letters!"

        if len(email) < 1:
            errors["email"] = "Email cannot be blank!"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid Email Address!"

        if len(password) < 1:
            errors["password"] = "Password cannot be blank!"
        elif len(password) < 8:
            errors["password"] = "Password must be at least 8 characters!"
        elif not PW_REGEX.match(password):
            errors["password"] = "Password is weak!"
        elif not confirm_pw:
            errors["confirm_pw"] = "Confirm Password cannot be blank!"
        elif (confirm_pw) and (confirm_pw != password):
            errors["confirm_pw"] = "Password doesn't match!"
        
        if len(errors) == 0:
            exists = User.objects.filter(email = email)

            if not len(exists):
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

                user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = pw_hash )
                response['user'] = user
            else:
                errors["email"] = "User already exists! Use new email address or login."

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        
        return response

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return "\n\tID: {}\n\tFirst Name: {}\n\tLast Name: {}\n\tEmail: {}\n".format(str(self.id), str(self.first_name), str(self.last_name), str(self.email))

    __repr__ = __str__