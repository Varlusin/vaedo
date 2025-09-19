from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class UserModel(AbstractUser):
    """
    Այս մոդելը **AbstractUser** ի մոդեռնիզացված տարբերակն է՝  այստեղ ավելացված է հեռախոսահամար պարտադիր  ինչպես նաև անուն և ազգանուն։
    """
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
    )
    phone =  PhoneNumberField(help_text = _('Phone number'), max_length=20)
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "email"]
