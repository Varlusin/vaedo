from django.db import models
from django.utils.translation import get_language
from modeltranslation.translator import translator

class TranslationQuerySet(models.QuerySet):

    def with_translations(self, language=None, fields=None):
        if language is None:
            language=get_language()
        model_class=self.model
        translatable_fields=set()
        if model_class in translator.get_registered_models():
            options=translator.get_options_for_model(model_class)
            translatable_fields = set(options.get_field_names())
        if fields is None:
            fields = translatable_fields
        selected_fields = ['id']
        for field in fields:
            if field in translatable_fields:
                selected_fields.append(f"{field}_{language}")
            else:
                selected_fields.append(field)
        return self.only(*selected_fields)

