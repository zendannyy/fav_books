from django.db import models
from datetime import date, datetime
import re


class UserManager(models.Manager):
    def user_validator(self, post_data):
        """validator for name, email, pw
        all key names come from form in index.html"""
        errors = {}
        if len(post_data['first_name']) < 3:
            errors["first_name"] = "Name should be at least 3 characters"
        if not post_data['last_name'].isalpha():
            errors["first_name"] = "Name should only be alphabetical characters"

        if len(post_data['last_name']) < 3:
            errors["last_name"] = "Name should be at least 3 characters"
        if not post_data['last_name'].isalpha():
            errors["first_name"] = "Name should only be alphabetical characters"

        email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not email_re.match(post_data['email']):
            errors['email'] = "Invalid email address"
        # return errors

        # for unique validation of emails, using filer since this can contain empty lists and won't break
        users_with_email = User.objects.filter(
            email=post_data['email'])
        if len(users_with_email) >= 1:
            errors['dupe'] = "Email is taken, choose another"

        if len(post_data['password']) < 12:
            errors['password'] = "Password is too short, 12 or more characters please"

        if post_data['password'] != post_data['confirm_password']:
            errors['match'] = "Password does not match password confirmation"
        return errors

    def book_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 5:
            errors['title'] = "Title must be 5 characters or more"
        if len(post_data['author']) < 5:
            errors['author'] = "Author cannot be blank, must be 5 characters or more"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(default='email',
                             max_length=20)
    password = models.CharField(default='password',
                                max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded",
                                    on_delete=models.CASCADE, null=True)
    liked_by = models.ManyToManyField(User, related_name="books_liked",
                                      null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
