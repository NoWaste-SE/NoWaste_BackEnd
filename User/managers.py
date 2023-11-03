from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


'''provide an interface to interact with MyAuthor model,set striction and check authentication'''
class AuthorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        """
        Retrieve a user by their email address for use in authentication.
        """
        return self.get(email=email)

'''Use restaurant manager for interact in our specific way with restaurants objects,other than basic model manager'''
class RestaurantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('myauthor_ptr')

    def update(self, id, **kwargs):
        restaurant = self.get_queryset().get(id=id)
        for key, value in kwargs.items():
            setattr(restaurant, key, value)
        restaurant.save()
        return restaurant

    def get(self, id):
        return self.get_queryset().get(id=id)
