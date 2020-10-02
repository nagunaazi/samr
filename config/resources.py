from import_export import resources
from .models import BankList


class BankListResource(resources.ModelResource):
    class Meta:
        model = BankList
        import_id_fields = ('Bank_id',)
        

