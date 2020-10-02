from django.contrib import admin
from .models import *
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin


from .resources import *



class ZVT_PORTAL_CIRAdmin(ImportExportModelAdmin):
   list_display = ('zvt_portal_cir_id',
'mandt',
'vbeln',
'posnr',
'gjahr',
'monat',
'vkorg',
'vtweg',
'spart',
'pstyv',
'sold_to_party',
'ship_to_party',
'ord_date',
'vgbel',
'bezei',
'drerz',
'pva',
'matnr',
'pub_name',
'soff_name',
'cg_name',
'sdist_name',
'edition_name',
'cust_name',
'city_name',
'vkgrp',
'sgrp_name',
'vkbur',
'kdgrp',
'bzirk',
'rate',
'disc_perc',
'discount',
'gross_copy',
'free_copy',
'paid_copy',
'zlao',
'zcoo',
'gross_value',
'net_value',
'route',
)
   search_fields = ('zvt_portal_cir_id',
'mandt',
'vbeln',
'posnr',
'gjahr',
'monat',
'vkorg',)
   list_filter   = ('vkorg',)
   resource_class = ZVT_PORTAL_CIRResource

admin.site.register(ZVT_PORTAL_CIR,ZVT_PORTAL_CIRAdmin)
