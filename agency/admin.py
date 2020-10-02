from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *



class TeamMasterAdmin(admin.ModelAdmin):
   list_display = ('team_id',
'state_id',
'unit_id',
'access_type',
'team_SAPcode',
'team_name',
'team_email'

)
   search_fields = ('team_SAPcode',

)
   list_filter   = ('team_SAPcode',
)

admin.site.register(TeamMaster,TeamMasterAdmin)



class StateMasterAdmin(admin.ModelAdmin):
   list_display = ('state_id', 
'state_code', 
'state_bscode', 
'state_name', 
'state_language',  
'state_area_in_km', 
'state_population', 
'status', 
'create_date', 
'update_date', 
'create_user', 
'update_user' 
)
   search_fields = ('state_code','state_bscode','state_name')
   list_filter   = ('state_code','state_bscode','status')

admin.site.register(StateMaster,StateMasterAdmin)




class UnitMasterAdmin(admin.ModelAdmin):
   list_display = ('unit_id', 
'state_id', 
'unit_code', 
'unit_name', 
'status', 
'create_date', 
'update_date', 
'create_user', 
'update_user' 
)
   search_fields = ('unit_code','unit_name')
   list_filter   = ('unit_code','unit_name')

admin.site.register(UnitMaster,UnitMasterAdmin)




class CityMasterAdmin(admin.ModelAdmin):
   list_display = ('city_id', 
'state_id', 
'unit_id', 
'city_code', 
'city_name', 
'city_area_in_km', 
'city_population', 
'status', 
'create_date', 
'update_date', 
'create_user', 
'update_user' 
)
   search_fields = ('city_code', 
'city_name', )
   list_filter   = ('city_code', 
'city_name', )

admin.site.register(CityMaster,CityMasterAdmin)


class LocationMasterAdmin(admin.ModelAdmin):
   list_display = ( 'location_id',
'city_id',
'unit_id',
'location_code',
'location_name',
'location_area_in_km',
'location_population',
'city_upc',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('location_code',
'location_name', )
   list_filter   = ( 'location_code',
'location_name',)

admin.site.register(LocationMaster,LocationMasterAdmin)


class TownMasterAdmin(admin.ModelAdmin):
   list_display = ( 'town_id',
'city_id',
'unit_id',
'town_code',
'town_name',
'town_area_in_km',
'town_population',
'status',
'create_date',
'update_date',
'create_user',
'update_user'


)
   search_fields = ('town_code',
'town_name', )
   list_filter   = ('town_code',
'town_name',)

admin.site.register(TownMaster,TownMasterAdmin)



class PlantMasterAdmin(admin.ModelAdmin):
   list_display = ('plant_id',
'plant_code',
'plant_name',
'state_id',
'unit_id',
'plant_location_lat',
'plant_location_long',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('plant_code',
'plant_name',)
   list_filter   = ('plant_code',
'plant_name',)

admin.site.register(PlantMaster,PlantMasterAdmin)








class RouteMasterAdmin(admin.ModelAdmin):
   list_display = ('route_id',
'route_code',
'route_name',
'plant_id',
'unit_id',
'city_upc',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('route_code',
'route_name',)
   list_filter   = ('route_code',
'route_name',)

admin.site.register(RouteMaster,RouteMasterAdmin)



class DroppingPointMasterAdmin(admin.ModelAdmin):
   list_display = ('dropping_id',
'dropping_name',
'route_id',
'dropping_location_lat',
'dropping_location_long',
'unit_id',
'city_upc',
'status',
'create_date',
'update_date',
'create_user',
'update_user'


)
   search_fields = ('dropping_name',
)
   list_filter   = ('dropping_name',
)

admin.site.register(DroppingPointMaster,DroppingPointMasterAdmin)



class PublicationMasterAdmin(admin.ModelAdmin):
   list_display = ('publication_id',
'publication_code',
'publication_name',
'publication_language',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('publication_code',
'publication_name',
)
   list_filter   = ('publication_code',
'publication_name',
)

admin.site.register(PublicationMaster,PublicationMasterAdmin)






class EditionMasterAdmin(admin.ModelAdmin):
   list_display = ('edition_id',
'publication_id',
'edition_code',
'edition_name',
'edition_language',
'status',
'create_date',
'update_date',
'create_user',
'update_user'


)
   search_fields = ('edition_code',
'edition_name',
)
   list_filter   = ('edition_code',
'edition_name',
)

admin.site.register(EditionMaster,EditionMasterAdmin)





class NewspaperMasterAdmin(admin.ModelAdmin):
   list_display = ('newspaper_id',
'newspaper_code',
'newspaper_name',
'newspaper_language',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('newspaper_code',
'newspaper_name',
)
   list_filter   = ('newspaper_code',
'newspaper_name',
)

admin.site.register(NewspaperMaster,NewspaperMasterAdmin)






class DepartmentMasterAdmin(admin.ModelAdmin):
   list_display = ('department_id',
'department_name',
'status',
'create_date',
'update_date',
'create_user',
'update_user'
)
   search_fields = ('department_name',

)
   list_filter   = ('department_name',
)

admin.site.register(DepartmentMaster,DepartmentMasterAdmin)





class AddressProofMasterAdmin(admin.ModelAdmin):
   list_display = ('addressproof_id',
'addressproof_name',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('addressproof_name',

)
   list_filter   = ('addressproof_name',
)

admin.site.register(AddressProofMaster,AddressProofMasterAdmin)





class CommissionMasterAdmin(admin.ModelAdmin):
   list_display = ('commission_id',
'unit_id',
'commission_per',
'commission_amt',
'valid_from',
'valid_to',
'status',
'create_date',
'update_date',
'create_user',
'update_user'


)
   search_fields = ('commission_per',
'commission_amt',

)
   list_filter   = ('commission_per',
'commission_amt',
)

admin.site.register(CommissionMaster,CommissionMasterAdmin)





class RealtionMasterAdmin(admin.ModelAdmin):
   list_display = ('relation_id',
'relation',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('relation',

)
   list_filter   = ('relation',
)

admin.site.register(RealtionMaster,RealtionMasterAdmin)



class MaritialStatusMasterAdmin(admin.ModelAdmin):
   list_display = ('maritial_id',
'maritial_status',
'status',
'create_date',
'update_date',
'create_user',
'update_user'

)
   search_fields = ('maritial_status',

)
   list_filter   = ('maritial_status',
)

admin.site.register(MaritialStatusMaster,MaritialStatusMasterAdmin)





