from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models import Q



class Client(models.Model):
    code = models.CharField(max_length = 50, blank = False, null = False, unique=True, verbose_name = "Código Interno")
    code_sap = models.CharField(max_length = 50, blank = False, null = False, unique=True, verbose_name = "Código SAP")
    ruc = models.CharField(max_length = 30, blank = True, null = True, unique=True, verbose_name = "Ruc")
    name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Nombre")
    business_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Razón social")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'client_user', blank = False, null = False) 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'client_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'client_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    def build_code(self):
        id_code = Client.objects.latest('id').id + 1
        code = 'CA' + str(id_code).zfill(5)
        return code
    
    def build_code_sap(self):
        code_sap = 'C' + str(self.ruc)
        return code_sap

    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = self.build_code()
            self.code_sap = self.build_code_sap()
        super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return self.name

class Location(models.Model):
    code = models.CharField(max_length = 50, blank = False, null = False, unique=True, verbose_name = "Código Interno")
    name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Nombre")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'location_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'location_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")
    
    def build_code(self):
        id_code = Location.objects.latest('id').id + 1
        code = 'ZO' + str(id_code).zfill(5)
        return code

    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = self.build_code()
        super(Location, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"
        ordering = ['name']

    def __str__(self):
        return self.name


class Plantation(models.Model):
    code = models.CharField(max_length = 50, blank = False, null = False, verbose_name = "Código Interno")
    name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Nombre")
    area = models.FloatField(blank = False, null = False, verbose_name = "Area")
    area_unit_me = models.CharField(max_length = 10, blank = False, null = False, verbose_name = "Unidad de Medida")
    client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name = 'client_plantations', blank = False, null = False, verbose_name = "Cliente") 
    location = models.ForeignKey(Location, on_delete = models.PROTECT, related_name = 'location_plantations', blank = False, null = False, verbose_name = "Zona")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    def build_code(self):
        id_code = Plantation.objects.latest('id').id + 1
        code = 'FA' + str(id_code).zfill(5)
        return code

    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = self.build_code()
        super(Plantation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Fundo"
        verbose_name_plural = "Fundos"
        ordering = ['name', 'location__name']
        unique_together = (('name', 'client'),)

    def __str__(self):
        return '%s-%s' % (self.client.code_sap, self.name)


class Crop(models.Model):
    code = models.CharField(max_length = 50, blank = False, null = False, unique=True, verbose_name = "Código Interno")
    name = models.CharField(max_length = 100, blank = False, null = False, unique=True, verbose_name = "Nombre")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'crop_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'crop_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    def build_code(self):
        id_code = Crop.objects.latest('id').id + 1
        code = 'CU' + str(id_code).zfill(5)
        return code

    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = self.build_code()
        super(Crop, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Cultivo"
        verbose_name_plural = "Cultivos"
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)


class CropVariety(models.Model):
    KIND_CHOICES = (
        ('1', 'Tradicional'),
        ('2', 'Nueva'),
    )

    code = models.CharField(max_length = 50, blank = False, null = False, verbose_name = "Código")
    name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Nombre")
    color = models.CharField(max_length = 50, blank = True, null = True, verbose_name = "Color")
    kind = models.CharField(max_length = 1, blank = True, null = True, choices=KIND_CHOICES, verbose_name = "Tipo")
    crop = models.ForeignKey(Crop, on_delete = models.CASCADE, related_name = 'crop_varieties', blank = False, null = False, verbose_name = "Cultivo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'crop_variety_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'crop_variety_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")
    cropVarietySimilar = models.ManyToManyField('self', blank = True,  verbose_name = "Cultivo Similar")


    def build_code(self):
        id_code = CropVariety.objects.latest('id').id + 1
        code = 'VA' + str(id_code).zfill(5)
        return code

    def save(self, *args, **kwargs):
        if self.id is None:
            self.code = self.build_code()
        super(CropVariety, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Variedad"
        verbose_name_plural = "Variedades"
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)


class PlantationDivision(models.Model):
    main_division = models.CharField(max_length = 200, blank = False, null = False, verbose_name = "División Principal")
    sub_division_1 = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Sub División 1")
    sub_division_2 = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Sub División 2")
    sub_division_3 = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Sub División 3")
    sub_division_4 = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Sub División [Sólo Ensayos]")
    acronymo_note = models.CharField(max_length = 30, blank = False, null = False, verbose_name = "Acrónimo Nota")
    acronymo_real = models.CharField(max_length = 30, blank =False, null = False, verbose_name = "Acrónimo Real")
    plantation = models.ForeignKey(Plantation, on_delete = models.CASCADE, related_name = 'plantation_divisions', blank = False, null = False, verbose_name = "Fundo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_division_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_division_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")


    class Meta:
        verbose_name = "Fundo [Lote]"
        verbose_name_plural = "Fundos [Lotes]"
        ordering = ['plantation','main_division', 'sub_division_1', 'sub_division_2', 'sub_division_3','sub_division_4']
        unique_together = (('plantation', 'main_division', 'sub_division_1', 'sub_division_2', 'sub_division_3', 'sub_division_4'),)

    def clean(self):
        """
        Checks that we do not create multiple categories with 
        no parent and the same name.
        """
        from django.core.exceptions import ValidationError
        if self.pk is None:
            if self.sub_division_1 is None and PlantationDivision.objects.filter(plantation=self.plantation, main_division=self.main_division, sub_division_1=None, sub_division_2=None, sub_division_3=None, sub_division_4=None).exists():
                raise ValidationError("Ya existe el fundo %s con esas divisiones %s" % (self.plantation , self.main_division))
            elif self.sub_division_2 is None and self.sub_division_1 is not None and self.sub_division_3 is None and self.sub_division_4 is None and PlantationDivision.objects.filter(plantation=self.plantation, main_division=self.main_division, sub_division_1=self.sub_division_1, sub_division_2=None, sub_division_3=None, sub_division_4=None).exists():
                raise ValidationError("Ya existe el fundo %s con esas divisiones %s" % (self.plantation , self.main_division))
            elif self.sub_division_3 is None and self.sub_division_1 is not None and self.sub_division_2 is not None and self.sub_division_4 is None and PlantationDivision.objects.filter(plantation=self.plantation, main_division=self.main_division, sub_division_1=self.sub_division_1, sub_division_2=self.sub_division_2, sub_division_3=None, sub_division_4=None).exists():
                raise ValidationError("Ya existe el fundo %s con esas divisiones %s" % (self.plantation , self.main_division))
            elif self.sub_division_4 is None and self.sub_division_1 is not None and self.sub_division_2 is not None and self.sub_division_3 is not None and PlantationDivision.objects.filter(plantation=self.plantation, main_division=self.main_division, sub_division_1=self.sub_division_1, sub_division_2=self.sub_division_2, sub_division_3=self.sub_division_3, sub_division_4=None).exists():
                raise ValidationError("Ya existe el fundo %s con esas divisiones %s" % (self.plantation , self.main_division))

    def __str__(self):
        return str(self.plantation) + "-" + self.acronymo_note
 

class PlantationDivisionVariety(models.Model):
    plantation_division = models.ForeignKey(PlantationDivision, on_delete = models.CASCADE, related_name = 'plantation_divisionsvariety', blank = False, null = False, verbose_name = "Fundo-Lote")
    crop_variety = models.ForeignKey(CropVariety, on_delete = models.CASCADE, related_name = 'plantation_cropsvariety', blank = False, null = False, verbose_name = "Variedad")
    change_date = models.DateField(blank = True, null = True, verbose_name = "Fecha de Cambio")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_division_variety_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'plantation_division_variety_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    class Meta:
        verbose_name = "Variedad [Lote]"
        verbose_name_plural = "Variedades [Lotes]"
        ordering = ['plantation_division', 'crop_variety', 'created_date']

    def __str__(self):
        return str(self.plantation_division) + "-" + str(self.crop_variety)

class LandInfo(models.Model):
    DOC_KIND_CHOICES = (
        ('1', 'Normal'),
        ('2', 'Ensayo'),
    )

    PHASE_CROP_CHOICES = (
        ('1', 'Producción'),
        ('2', 'Formación'),
    )

    plantation = models.ForeignKey(Plantation, on_delete = models.PROTECT, related_name = 'plantation_land_info', blank = False, null = False, verbose_name = "Fundo")
    doc_name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Documento")
    file = models.FileField(upload_to='images',  null = False, blank = False, validators=[FileExtensionValidator(allowed_extensions=['docx'])], verbose_name = "Documento Word")
    doc_kind = models.CharField(max_length = 1, blank = False, null = False, choices=DOC_KIND_CHOICES, verbose_name = "Tipo de estudio")
    phase_crop = models.CharField(max_length = 1, blank = True, null = True, choices=PHASE_CROP_CHOICES, verbose_name = "Etapa del cultivo")
    comments = models.CharField(max_length = 1000, blank = True, null = True, verbose_name = "Comentarios")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'land_info_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'land_info_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    class Meta:
        verbose_name = "Vuelo [Carga Doc]"
        verbose_name_plural = "Vuelos [Carga Doc]"
        ordering = ['plantation']

    def __str__(self):
        return '%s-%s' % (self.doc_name, self.plantation)

class Land(models.Model):
    plantation_division_variety = models.ForeignKey(PlantationDivisionVariety, on_delete = models.PROTECT, related_name = 'plantationlands_divisionvariety', blank = False, null = False, verbose_name = "Fundo/Cuartel/Variedad")
    flight_number = models.IntegerField(blank = True, null = True, verbose_name = "Número de vuelo")
    date = models.DateField(blank = False, null = False, verbose_name = "Fecha de la foto")
    kind_proccess = models.CharField(max_length = 50, blank = False, null = False, verbose_name = "Tipo de proceso")
    days_process = models.IntegerField(blank = False, null = False, verbose_name = "Dias despues del proceso")
    is_test = models.BooleanField(blank = False, null = False, default = False, verbose_name = "¿Es testigo?")
    comments = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Comentarios")
    applied_product= models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Producto aplicado")
    url_image = models.ImageField(upload_to='images',  null = False, blank = False, validators=[FileExtensionValidator(allowed_extensions=['png'])], verbose_name = "Foto lote")
    url_external = models.CharField(max_length = 800, blank = False, null = False, verbose_name = "Url externa")
    json_name = models.CharField(max_length = 200, blank = False, null = False, verbose_name = "Nombre json")
    land_info = models.ForeignKey(LandInfo, on_delete = models.CASCADE, related_name = 'land_land_info', blank = False, null = False, verbose_name = "Nombre documento")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'land_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'land_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")


    class Meta:
        verbose_name = "Vuelo [Foto]"
        verbose_name_plural = "Vuelos [Fotos]"
        ordering = ['plantation_division_variety__plantation_division__plantation']
        unique_together = (('plantation_division_variety', 'date', 'kind_proccess', 'days_process'),)

    def __str__(self):
        return str(self.plantation_division_variety)


class Ndvi(models.Model):

    COLOR_CHOICES = (
        ('1', 'Verde'),
        ('2', 'Amarillo'),
        ('3', 'Anaranjado'),
        ('4', 'Anaranjado Oscuro'),
        ('5', 'Rojo'),
    )
    CLASE_CHOICES = (
        ('1', 'Muy Bueno'),
        ('2', 'Bueno'),
        ('3', 'Regular'),
        ('4', 'Deficitario'),
        ('5', 'Muy Deficitario'),
    )
    color = models.CharField(max_length = 1, blank = False, null = False, choices=COLOR_CHOICES, verbose_name = "Color")
    clase = models.CharField(max_length = 1, blank = False, null = False, choices=CLASE_CHOICES,  verbose_name = "Clase")
    min = models.FloatField(blank = False, null = False, verbose_name = "Minimo")
    max = models.FloatField(blank = False, null = False, verbose_name = "Maximo")
    ha = models.FloatField(blank = False, null = False, verbose_name = "Hectarea")
    area = models.FloatField(blank = False, null = False, verbose_name = "% Hectarea")
    land = models.ForeignKey(Land, on_delete = models.CASCADE, related_name = 'land_ndvis', blank = False, null = False, verbose_name = "Fundo-División-Variedad")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'ndvi_created_by', blank = False, null = False, verbose_name = "Creado por")
    created_date = models.DateTimeField(auto_now_add = True, verbose_name = "Fecha de Creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'ndvi_modified_by', blank = True, null = True, verbose_name = "Modificado por")
    modified_date = models.DateTimeField(blank = True, null = True, verbose_name = "Fecha Modificación")

    class Meta:
        verbose_name = "Vuelo [NDVIs]"
        verbose_name_plural = "Vuelos [NDVIs]"
        unique_together = (('color', 'clase', 'min', 'max', 'ha', 'area', 'land'),)


    def __str__(self):
        return str(self.id)


class PlantationDivisionVarietyTmp(models.Model):
    unit_me = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Unidad Medida")
    variety = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Variedad")
    plantation = models.ForeignKey(Plantation, on_delete = models.PROTECT, related_name = 'plantation_division_variety_temps', blank = False, null = False)
    unit_me_equi = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Unidad Medida Equi")
    variety_equi = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Variedad Equi")

    class Meta:
        verbose_name_plural = "plantationdivisionvariety_temps"
        unique_together = (('unit_me', 'variety', 'plantation'),)

    def __str__(self):
        return str(self.id)



class LandTmp(models.Model):
    plantation_division_variety_tmp = models.ForeignKey(PlantationDivisionVarietyTmp, on_delete = models.CASCADE, related_name = 'plantationlands_divisionv_variety_temps', blank = True, null = True) # Asociación con el fundo
    date = models.DateField(blank = False, null = False) #Fecha de la foto
    kind_proccess = models.CharField(max_length = 50, blank = False, null = False, verbose_name = "Tipo de proceso") # DDC, DDP O DDS
    days_process = models.IntegerField(blank = False, null = False, verbose_name = "Dias despues del proceso") #57
    comments = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Es un ensayo") # comentarios
    is_test = models.BooleanField(blank = False, null = False, default = False) # Es un ensayo
    applied_product= models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Producto aplicado") # Producto aplicado 
    flight_number = models.IntegerField(blank = False, null = False, verbose_name = "Numero de vuelo") # Número de vuelo 1,2,3,4
    url_image = models.ImageField(upload_to='images',  null = True, blank = True, validators=[FileExtensionValidator(allowed_extensions=['png'])], verbose_name = "Archivo") #URL de la imagen
    total_area = models.FloatField(blank = False, null = False, verbose_name = "Total Area") # total_area
    doc_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Documento") # Documento
    json_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Json Name") # Documento
    
    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ['id']

    def __str__(self):
        return str(self.id)


class NdviTmp(models.Model):
    color = models.CharField(max_length = 30, blank = False, null = False, verbose_name = "Color") #Color 'Verde', 'Amarillo', 'Anaranjado', 'Anaranjado Oscuro', 'Rojo'
    clase = models.CharField(max_length = 30, blank = False, null = False, verbose_name = "Clase") # 'Muy Bueno', 'Bueno', 'Regular', 'Deficitario', 'Muy Deficitario'
    min = models.FloatField(blank = False, null = False, verbose_name = "Minimo") # Minimo
    max = models.FloatField(blank = False, null = False, verbose_name = "Maximo") # Maximo
    ha = models.FloatField(blank = False, null = False, verbose_name = "Hectarea") # Hectarea
    area = models.FloatField(blank = False, null = False, verbose_name = "Porcenteja Hectarea") #%Hectarea
    land_tmp = models.ForeignKey(LandTmp, on_delete = models.CASCADE, related_name = 'land_ndvis_temps', blank = False, null = False) #Relacion con el land

    class Meta:
        verbose_name_plural = "Ndvis"
        unique_together = (('color', 'clase', 'min', 'max', 'ha', 'area', 'land_tmp'),)


    def __str__(self):
        return str(self.id)
    
    
class DocPhaseTmp(models.Model):
    doc_name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = "Documento") # Documento
    phase_name = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Fase") # Documento
    phase_is = models.IntegerField(blank = True, null = True, verbose_name = "Fase ID") #57
    
    class Meta:
        verbose_name = "DocPhaseTmp"
        verbose_name_plural = "DocPhaseTmps"
        ordering = ['id']

    def __str__(self):
        return str(self.id)




