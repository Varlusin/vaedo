from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import URLValidator
from vaedo.managers import TranslationQuerySet

class TypefuturQuerySet(TranslationQuerySet):
    def published(self):
        return self.filter(publish=True).order_by('-id')

    def by_slug(self, slug):
        return self.published().filter(slug=slug)


class FuturQuerySet(TranslationQuerySet):
    def published(self):
        return self.filter(publish=True).order_by('-id')

    def by_slug(self, slug):
        return self.published().filter(slug=slug)



class Typefutur(models.Model):

    futurtype = models.CharField(max_length=50, unique=True, null=False)
    slug = models.SlugField(max_length=50, unique=True, null=False)
    publish = models.BooleanField()

    objects = TypefuturQuerySet.as_manager()

    class Meta:
        verbose_name = _("Type Futur")
        verbose_name_plural = _("Type Futures")

    def __str__(self):
        return f"{self.futurtype}"


class Futur(models.Model):
    category = models.ForeignKey(
        to=Typefutur, on_delete=models.PROTECT, related_name="futur"
    )
    names = models.CharField(max_length=50, unique=True)
    descriptions = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, null=False)
    img = models.ImageField(
        upload_to="futur_img", null=True, blank=True, default="default.jpg"
    )
    url = models.TextField(
        validators=[URLValidator()],
        max_length = 200, 
        blank=True, 
        null=True, ) 
    publish = models.BooleanField()

    objects = FuturQuerySet.as_manager()

    class Meta:
        verbose_name = _("Futur")
        verbose_name_plural = _("Futurs")

    def __str__(self):
        return f"{self.names}"

    def get_url(self):
        return reverse(
            "futur_detail",
            kwargs={"category_slug": self.category.slug, "futur_slug": self.slug},
        )


def pre_save_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.names if sender == Futur else instance.futurtype
        )


pre_save.connect(pre_save_slug_generator, sender=Typefutur)
pre_save.connect(pre_save_slug_generator, sender=Futur)

