from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        email=self.normalize_email(email)
        user=self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff should be True to be a superuser")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser has to be True")
        return self.create_user(email=email,password=password,**extra_fields)



class User(AbstractUser):
    email=models.CharField(unique=True,max_length=80)
    username=models.CharField(max_length=45)
    date_of_birth=models.DateField(null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Book(models.Model):
    name=models.CharField(max_length=150)
    author=models.CharField(max_length=140)
    volume = models.PositiveIntegerField(max_length=55)
    pages = models.IntegerField(null=True, blank=True)
    quantity=models.PositiveIntegerField(default=1)




    def __str__(self):
        return self.name
    @property
    def is_available(self):
        if self.quantity<1:
            return False
        else:
            return True

class IssueBook(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

