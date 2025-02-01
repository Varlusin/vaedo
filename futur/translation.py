from modeltranslation.translator import translator, TranslationOptions
from futur.models import Typefutur, Futur


class TypefuturTranslationOptions(TranslationOptions):
    fields= ('futurtype',)
translator.register(Typefutur, TypefuturTranslationOptions)


class FuturTranslationOptions(TranslationOptions):
    fields= ('names', 'descriptions')
translator.register(Futur, FuturTranslationOptions)