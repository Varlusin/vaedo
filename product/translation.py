from modeltranslation.translator import translator, TranslationOptions
from product.models import ProductCategory, Product


class ProductCategoryTranslationOptions(TranslationOptions):
    fields= ('type_product',)
translator.register(ProductCategory, ProductCategoryTranslationOptions)

class ProductTranslationOptions(TranslationOptions):
    fields= ('product_name',)
translator.register(Product, ProductTranslationOptions)