from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from leaflet.admin import LeafletGeoAdmin
from location.models import (
    locationAvailable,
    Street,
    Building,
    CustomerAddresses
)


class locationAvailableAdmin(LeafletGeoAdmin):
    pass

class locationAvailableTranslationAdmin(locationAvailableAdmin, TranslationAdmin):

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



class StreetAdmin(LeafletGeoAdmin):
    pass

class StreetTranslationAdmin(StreetAdmin, TranslationAdmin):

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class BuildingAdmin(LeafletGeoAdmin):
    pass


class CustomerAddressesleAdmin(LeafletGeoAdmin):
    pass

class CustomerAddressesTranslationAdmin(CustomerAddressesleAdmin, TranslationAdmin):

    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(locationAvailable, locationAvailableTranslationAdmin)
admin.site.register(Street, StreetTranslationAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(CustomerAddresses, CustomerAddressesTranslationAdmin)


