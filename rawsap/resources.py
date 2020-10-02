from import_export import resources
from .models import *


class ZVT_PORTAL_CIRResource(resources.ModelResource):
    class Meta:
        model = ZVT_PORTAL_CIR
        import_id_fields = ('zvt_portal_cir_id',)
        

