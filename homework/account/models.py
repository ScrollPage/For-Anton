from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password = None):
        user = self.model(
            email=self.normalize_email(email),
			username=username,
        )

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, username, password = None):
        user = self.create_user(
            email=self.normalize_email(email),
			username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using = self._db)

        return user

class Account(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField('Почтовый адрес', max_length = 60, unique = True)
	username = models.CharField('Имя пользователя', max_length=30)
	date_joined = models.DateTimeField(verbose_name = "date joined", auto_now_add = True)
	last_login = models.DateTimeField(verbose_name = "last_login", auto_now = True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	avatar = models.ImageField(upload_to="user_avatars/%Y/%m/%d", blank=True)
	is_active = models.BooleanField(default=True)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def get_url(self):
		try:
			return self.avatar.url
		except ValueError:
			return None