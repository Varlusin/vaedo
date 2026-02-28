from django.db import models
from django.utils.translation import gettext as _
# from grups.models import Company


class ProductCategory(models.Model):
    """
    Մոդելը ապրանքի տեսակի ցուցակ է ստեղծում՝
    1. **type_product** -> սա ապրանքի տեսակն է։ Օր՝ ըմպելիք, սուշի, սետեր։
    1. **slug** -> Սա հատուկ փոփոխական է orm հարցման ֆիլտռներ կիրառելու համար
    1. **image** ->
    """

    type_product = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="product_category_img", blank=True, null=True)

    class Meta:
        verbose_name = _("Type Product")
        verbose_name_plural = _("Types Product")

    def __str__(self) -> str:
        return f"{self.type_product} {self.slug}"


class Product(models.Model):
    """
    Մոդելը ապրանքի ցուցակ է ստեղծում՝
    1. **product_name** ->ապրանքի անունն է։ Օր՝ կոկա֊կոլա, շաուրմա խորոված ․․․․ ։
    1. **slug** -> Սա հատուկ փոփոխական է orm հարցման ֆիլտռներ կիրառելու համար։
    1. **img** -> ապրանքի նկարն է ։
    1. **category** -> **ProductCategory** մոդելի id-ն է այդ ապրանքի համար։
    1. **price** -> սա ?????? հարցն այն է որ հնարաոր է նույն ապրանքը տարբեր ընկերություններ շատ տարբեր գների վաճառեն։ ուստի ենթադրվում է որ ամեն ընկերություն իր առանձին աղյուսակը պետք է ունենա ապրանքների համար
    1. **discount** -> զեղջի չափն է։ եթե առկա է։ հակառակ դեպքում null
    1. **preparation_time** -> Եթե ապրանքը պատրաստովի է սա այն ժամանակն է որի ընթացքում մոտաոր ապրանքը պատրաստ կլինե եթե պատռաստի ապրանք է null:
    1. **count** -> սա ապրանքի քանաքն է որը առկա է եթե ապրանքը պատրաստովի է null
    """

    product_name = models.CharField(max_length=50)
    img = models.ImageField(upload_to="product_img")
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.PROTECT, related_name="product_type"
    )
    price = models.FloatField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    preparation_time = models.TimeField(blank=True, null=True)
    count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return f"{self.product_name}"
