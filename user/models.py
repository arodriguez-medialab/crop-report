from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _

from django.utils import timezone


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(username, password=None, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):

    email = None
    password = None
	# Some rules adding username
    username_validator = UnicodeUsernameValidator()
	
	#Custom Field
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Requerido. 150 caracteres o menos. Letras, digitos y @/./+/-/_ solamente.'),
        validators=[username_validator],
        error_messages={
            'unique': _("El existe un usuario con el mismo nombre."),
        },
        blank=True # Same code that has django as a default only added this to say can be an empty value
    )
    
    # All these field declarations are copied as-is
    # from `AbstractUser`
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['username', 'last_name']

    # Add additional fields here if needed

    objects = UserManager()

    USERNAME_FIELD = 'username'