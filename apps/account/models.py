from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,name,email,phone_number,password):

        if not email:
            raise ValueError('You Must got email')

        if not name:
            raise ValueError('You Must got name')

        if not phone_number:
            raise ValueError('You Must got phone_number')

        if not password:
            raise ValueError('You Must got password')


        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,phone_number,password):
        if not email:
            raise ValueError('You Must got email')

        if not name:
            raise ValueError('You Must got name')

        if not phone_number:
            raise ValueError('You Must got phone_number')

        if not password:
            raise ValueError('You Must got password')


        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            is_admin=True,
            is_superuser=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13)
    is_admin = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ('name','phone_number')

    def __str__(self):
        return str(self.name)

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin