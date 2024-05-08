from django.contrib import admin
from plantation.models import Land, Ndvi, Client, Location, Plantation, Crop, CropVariety, PlantationDivision, PlantationDivisionVariety
from datetime import datetime
from plantation.custom_admin_functions import custom_titled_filter
from django.utils.html import format_html


# Register your models here.

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ["id", "flight_number", "get_plantation", "get_crop_variety", "get_division", "date", "kind_proccess", "days_process",'url_image', 'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['date']
    list_filter = ('plantation_division_variety__plantation_division__plantation', 'plantation_division_variety__crop_variety', 'kind_proccess', 'days_process', 'flight_number' )
    exclude = ['json_name', 'created_by', 'modified_by', 'created_date', 'modified_date']
    list_per_page = 25
    raw_id_fields = ['plantation_division_variety']

    def get_plantation(self, obj):
        return format_html(u'<a href="/admin/plantation/plantation/%s/">%s</a>' % (obj.plantation_division_variety.plantation_division.plantation.id, obj.plantation_division_variety.plantation_division.plantation))
    get_plantation.short_description = 'Fundo'
    get_plantation.admin_order_field = 'plantation_division_variety__plantation_division__plantation'
    get_plantation.allow_tags = True

    def get_division(self, obj):
        return format_html(u'<a href="/admin/plantation/plantationdivision/%s/">%s</a>' % (obj.plantation_division_variety.plantation_division.id, obj.plantation_division_variety.plantation_division.main_division))
    get_division.short_description = 'Lote'
    get_division.admin_order_field = 'plantation_division_variety__plantation_division__main_division'
    get_division.allow_tags = True

    def get_crop_variety(self, obj):
        return format_html(u'<a href="/admin/plantation/cropvariety/%s/">%s</a>' % (obj.plantation_division_variety.crop_variety.id, obj.plantation_division_variety.crop_variety))
    get_crop_variety.short_description = 'Variedad'
    get_crop_variety.admin_order_field = 'plantation_division_variety__crop_variety'
    get_crop_variety.allow_tags = True

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)

@admin.register(Ndvi)
class NdviAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_plantation', 'get_division', 'get_crop_variety', 'color', 'clase', 'min', 'max', 'ha', 'area']
    list_per_page = 25
    list_filter = ('land__plantation_division_variety__plantation_division__plantation', 'land__plantation_division_variety__crop_variety', 'color',)
    exclude = ['created_by', 'modified_by', 'created_date', 'modified_date']
    raw_id_fields = ['land']

    #def has_delete_permission(self, request, obj=None):
    #    return False

    def has_add_permission(self, request):
        return False

    def get_plantation(self, obj):
        return format_html(u'<a href="/admin/plantation/plantation/%s/">%s</a>' % (obj.land.plantation_division_variety.plantation_division.plantation.id, obj.land.plantation_division_variety.plantation_division.plantation))
    get_plantation.short_description = 'Fundo'
    get_plantation.admin_order_field = 'land__plantation_division_variety__plantation_division__plantation'
    get_plantation.allow_tags = True

    def get_division(self, obj):
        return format_html(u'<a href="/admin/plantation/plantationdivision/%s/">%s</a>' % (obj.land.plantation_division_variety.plantation_division.id, obj.land.plantation_division_variety.plantation_division.main_division))
    get_division.short_description = 'Lote'
    get_division.admin_order_field = 'land__plantation_division_variety__plantation_division__main_division'
    get_division.allow_tags = True

    def get_crop_variety(self, obj):
        return format_html(u'<a href="/admin/plantation/cropvariety/%s/">%s</a>' % (obj.land.plantation_division_variety.crop_variety.id, obj.land.plantation_division_variety.crop_variety))
    get_crop_variety.short_description = 'Variedad'
    get_crop_variety.admin_order_field = 'land__plantation_division_variety__crop_variety'
    get_crop_variety.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "ruc", "business_name", "code", "code_sap",'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['name']
    search_fields = ["code_sap", 'name', 'ruc', 'business_name']
    list_per_page = 25
    exclude = ['code', "code_sap", 'created_by', 'modified_by', 'created_date', 'modified_date']

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['name']
    search_fields = ['name']
    list_per_page = 25
    exclude = ['code', 'created_by', 'modified_by', 'created_date', 'modified_date']

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)


@admin.register(Plantation)
class PlantationAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "area", "area_unit_me", "get_client", "code", 'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['name', 'client']
    search_fields = ['name', 'client__name']
    list_filter = (("location", custom_titled_filter('Zona')),)
    list_per_page = 25
    exclude = ['code', 'created_by', 'modified_by', 'created_date', 'modified_date']

    def get_client(self, obj):
        return format_html(u'<a href="/admin/plantation/client/%s/">%s</a>' % (obj.client.id, obj.client))
    get_client.short_description = 'Cliente'
    get_client.admin_order_field = 'plantation__client'
    get_client.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ["name", "code",'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['name']
    list_filter = ("name",)
    exclude = ['code', 'created_by', 'modified_by', 'created_date', 'modified_date']

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)


@admin.register(CropVariety)
class CropVarietyAdmin(admin.ModelAdmin):
    list_display = ["name", "crop", "kind", "color", 'code', 'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['name']
    list_per_page = 50
    list_filter = ('crop', 'name', 'kind')
    exclude = ['code','created_by', 'modified_by', 'created_date', 'modified_date']
    filter_horizontal = ('cropVarietySimilar',)

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)


@admin.register(PlantationDivision)
class PlantationDivisionAdmin(admin.ModelAdmin):
    list_display = ("id", "get_url_plantation", "get_client", "main_division", "sub_division_1", "sub_division_2", "sub_division_3", "sub_division_4", "acronymo_note", "acronymo_real",)
    ordering = ['plantation', 'main_division']
    list_per_page = 50
    list_filter = ('plantation',)
    exclude = ['acronymo_real','created_by', 'modified_by', 'created_date', 'modified_date']
    list_editable = ('acronymo_note', )

    def get_url_plantation(self, obj):
        return format_html(u'<a href="/admin/plantation/plantation/%s/">%s</a>' % (obj.plantation.id, obj.plantation))
    get_url_plantation.short_description = 'Fundo'
    get_url_plantation.admin_order_field = 'plantation'
    get_url_plantation.allow_tags = True

    def get_client(self, obj):
        return format_html(u'<a href="/admin/plantation/client/%s/">%s</a>' % (obj.plantation.client.id, obj.plantation.client))
    get_client.short_description = 'Cliente'
    get_client.admin_order_field = 'plantation__client'
    get_client.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.acronymo_real = str(obj.acronymo_note).strip().replace(" ", "").lower()
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)

@admin.register(PlantationDivisionVariety)
class PlantationDivisionVarietyAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_plantation', 'get_division', 'get_crop_variety', 'get_acronymo_note', 'change_date', 'created_date']
    ordering = ['id']
    list_filter = ('plantation_division__plantation', 'crop_variety', )
    exclude = ['created_by', 'modified_by', 'created_date', 'modified_date']
    list_per_page = 25

    def get_plantation(self, obj):
        return format_html(u'<a href="/admin/plantation/plantation/%s/">%s</a>' % (obj.plantation_division.plantation.id, obj.plantation_division.plantation.name))
    get_plantation.short_description = 'Fundo'
    get_plantation.admin_order_field = 'plantation_division__plantation'

    def get_division(self, obj):
        return format_html(u'<a href="/admin/plantation/plantationdivision/%s/">%s</a>' % (obj.plantation_division.id, obj.plantation_division.main_division))
    get_division.short_description = 'División'
    get_division.admin_order_field = 'plantation_division__main_division'

    def get_acronymo_note(self, obj):
        return format_html(u'<a href="/admin/plantation/plantationdivision/%s/">%s</a>' % (obj.plantation_division.id, obj.plantation_division.acronymo_note))
    get_acronymo_note.short_description = 'Acrónimo Nota'
    get_acronymo_note.admin_order_field = 'plantation_division__main_division'

    def get_crop_variety(self, obj):
        return format_html(u'<a href="/admin/plantation/cropvariety/%s/">%s</a>' % (obj.crop_variety.id, obj.crop_variety.name))
    get_crop_variety.short_description = 'Variedad'
    get_crop_variety.admin_order_field = 'plantation_division__crop_variety'

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.created_by = request.user
            obj.created_date = datetime.now()
        else:
            obj.modified_by = request.user
            obj.modified_date = datetime.now()

        super().save_model(request, obj, form, change)
