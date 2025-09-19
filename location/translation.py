from django.forms import fields
from modeltranslation.translator import translator, TranslationOptions
from location.models import (
    locationAvailable,
    Street,
    CustomerAddresses
)


class locationAvailableTranslationOptions(TranslationOptions):
    fields= ('sity',)
translator.register(locationAvailable, locationAvailableTranslationOptions)


class StreetTranslationOptions(TranslationOptions):
    fields= ('name',)
translator.register(Street, StreetTranslationOptions)

class CustomerAddressesTranslationOptions(TranslationOptions):
    fields = ('adres',)
translator.register(CustomerAddresses, CustomerAddressesTranslationOptions)