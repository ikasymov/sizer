from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser



class MainUserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=None, **kwargs):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        if is_active is not None:
            user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MainUser(AbstractUser):
    username = models.CharField(max_length=100, blank=False, unique=True,
                                db_index=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True,)
    password = models.CharField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    avatar = models.CharField(max_length=500, blank=True, null=True)

    objects = MainUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True