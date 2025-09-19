from django.db import models
from django.contrib.gis.db import models as gismodels

from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import gettext as _
from datetime import datetime
from accaunts.models import UserModel

class locationAvailable(gismodels.Model):
    """այն քաղաքներն են որտեղ հասանելի է ծառայությունը։ 
    sity։քաղաքի անվանումը, geometry multypolygon քաղաքի մակերեսը։ """
    sity = models.CharField(max_length = 50 , db_index = True)
    geometry=gismodels.MultiPolygonField()
    # objects = gismodels.Manager()

    class Meta:
        # indexes=[
        #     GinIndex(name = 'NewGinIndex',fields=['sity'])
        # ]
        verbose_name = _("Բնակավայր")
        verbose_name_plural = _("Բնակավայրեր")

    def __str__(self):
        return self.sity




class Street(gismodels.Model):
    """ ճանապարհների աղյուսակ՝ name` անվանումը։ geometry: ճահապարհի կորդինատները """
    sity = models.ForeignKey(to=locationAvailable,
                             on_delete=models.PROTECT, 
                             related_name = 'street')
    name = models.CharField(max_length = 200, blank=True, null=True,  db_index = True)
    geometry = gismodels.MultiLineStringField( blank=True, null=True)

    class Meta:
        # indexes=[
        #     GinIndex(name = 'NewGinIndex',fields=['name'])
        # ]
        verbose_name = _("Ճանապարհ")
        verbose_name_plural = _("Ճանապարներ")
    def __str__(self):
        return self.name
    


class Building(gismodels.Model):
    """ շինություն պարունակում է sity->քաղաքի աղյուսակ stret -> ճահապարհի աղյուսակ 
     adres -> շինության Հասցեն center_point -> շինության կենտրոնը։ geometry -> շինության պոլիգոնը։ """
    sity = models.ForeignKey(to=locationAvailable,
                             on_delete=models.PROTECT, 
                             related_name = 'buildings')
    
    stret = models.ForeignKey(to=Street,
                             on_delete=models.PROTECT, 
                             related_name = 'buildings')
    adres = models.CharField(max_length = 70, blank=True, null = True, db_index = True)
    district = models.FloatField(blank=True, null=True)
    center_point = gismodels.PointField()
    geometry=gismodels.PolygonField()

    class Meta:
        indexes = [
            models.Index(fields=["sity", "district"]),  # Համակցված ինդեքս
            GinIndex(fields=["geometry"]),  # Գեոմետրիկ ինդեքս
        ]
        verbose_name = _("Շինություն")
        verbose_name_plural = _("Շինություններ")

    def __str__(self):
        return self.adres

class CustomerAddresses(gismodels.Model):
    """ 
    useri կատարած պատվերների հասցեներն է:
    custumer -> user id:
    building -> եթե հասցեն հայտնի է building աղյուսակում building ֊ի id֊ն եթե ոչ դատարկ արժեք:
    date -> հասցեն ընտրելու ժամանակն է։
    adres -> հասցեի անվանումն է: 
    geometry -> պատվերի հասցեի կորդինատները:  
    """
    custumer= models.ForeignKey(to=UserModel,
                                on_delete=models.PROTECT, 
                                related_name = 'order_adres')
    building = models.BigIntegerField(blank=True, null=True,)
    adres = models.CharField(max_length=70, blank=True, null=True)
    createOrUpdateDate = models.DateTimeField(default=datetime.now, blank=True) #auto_now_add = True)
    geometry = gismodels.PointField(blank=True, null = True, srid=4326)  
    
    def save(self, *args,  **kwargs):
        self.createOrUpdateDate = datetime.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Պատվիրված հասցե')
        verbose_name_plural = _('Պատվիրված հասցեններ')
    
    def __str__(self) -> str:
        return self.adres