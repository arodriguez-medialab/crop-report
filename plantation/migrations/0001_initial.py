# Generated by Django 4.0.3 on 2022-04-13 16:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Código Interno')),
                ('code_sap', models.CharField(max_length=50, unique=True, verbose_name='Código SAP')),
                ('ruc', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Ruc')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('business_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Razón social')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Código Interno')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Cultivo',
                'verbose_name_plural': 'Cultivos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CropVariety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Código')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                ('kind', models.CharField(blank=True, choices=[('1', 'Tradicional'), ('2', 'Nueva')], max_length=1, null=True, verbose_name='Tipo')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Variedad',
                'verbose_name_plural': 'Variedades',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Land',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha de la foto')),
                ('kind_proccess', models.CharField(max_length=50, verbose_name='Tipo de proceso')),
                ('days_process', models.IntegerField(verbose_name='Dias despues del proceso')),
                ('is_test', models.BooleanField(default=False, verbose_name='¿Es testigo?')),
                ('comments', models.CharField(blank=True, max_length=100, null=True, verbose_name='Comentarios')),
                ('applied_product', models.CharField(blank=True, max_length=100, null=True, verbose_name='Producto aplicado')),
                ('url_image', models.ImageField(upload_to='images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])], verbose_name='Foto lote')),
                ('url_external', models.CharField(max_length=800, verbose_name='Url externa')),
                ('json_name', models.CharField(max_length=200, verbose_name='Nombre json')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Vuelo [Foto]',
                'verbose_name_plural': 'Vuelos [Fotos]',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LandInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.IntegerField(verbose_name='Numero de vuelo')),
                ('doc_name', models.CharField(max_length=100, verbose_name='Documento')),
                ('file', models.FileField(upload_to='images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['docx'])], verbose_name='Documento Word')),
                ('doc_kind', models.CharField(choices=[('1', 'Normal'), ('2', 'Ensayo')], max_length=1, verbose_name='Tipo de estudio')),
                ('phase_crop', models.CharField(blank=True, choices=[('1', 'Producción'), ('2', 'Formación')], max_length=1, null=True, verbose_name='Etapa del cultivo')),
                ('comments', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comentarios')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Vuelo [Carga Doc]',
                'verbose_name_plural': 'Vuelos [Carga Doc]',
                'ordering': ['plantation'],
            },
        ),
        migrations.CreateModel(
            name='LandTmp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('kind_proccess', models.CharField(max_length=50, verbose_name='Tipo de proceso')),
                ('days_process', models.IntegerField(verbose_name='Dias despues del proceso')),
                ('comments', models.CharField(max_length=100, verbose_name='Es un ensayo')),
                ('is_test', models.BooleanField(default=False)),
                ('applied_product', models.CharField(max_length=100, verbose_name='Producto aplicado')),
                ('flight_number', models.IntegerField(verbose_name='Numero de vuelo')),
                ('url_image', models.ImageField(blank=True, null=True, upload_to='images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])], verbose_name='Archivo')),
                ('total_area', models.FloatField(verbose_name='Total Area')),
                ('doc_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Documento')),
                ('json_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Json Name')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Código Interno')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zonas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Ndvi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('1', 'Verde'), ('2', 'Amarillo'), ('3', 'Anaranjado'), ('4', 'Anaranjado Oscuro'), ('5', 'Rojo')], max_length=1, verbose_name='Color')),
                ('clase', models.CharField(choices=[('1', 'Muy Bueno'), ('2', 'Bueno'), ('3', 'Regular'), ('4', 'Deficitario'), ('5', 'Muy Deficitario')], max_length=1, verbose_name='Clase')),
                ('min', models.FloatField(verbose_name='Minimo')),
                ('max', models.FloatField(verbose_name='Maximo')),
                ('ha', models.FloatField(verbose_name='Hectarea')),
                ('area', models.FloatField(verbose_name='% Hectarea')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Vuelo [NDVIs]',
                'verbose_name_plural': 'Vuelos [NDVIs]',
            },
        ),
        migrations.CreateModel(
            name='NdviTmp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=30, verbose_name='Color')),
                ('clase', models.CharField(max_length=30, verbose_name='Clase')),
                ('min', models.FloatField(verbose_name='Minimo')),
                ('max', models.FloatField(verbose_name='Maximo')),
                ('ha', models.FloatField(verbose_name='Hectarea')),
                ('area', models.FloatField(verbose_name='Porcenteja Hectarea')),
            ],
            options={
                'verbose_name_plural': 'Ndvis',
            },
        ),
        migrations.CreateModel(
            name='Plantation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Código Interno')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('area', models.FloatField(verbose_name='Area')),
                ('area_unit_me', models.CharField(max_length=10, verbose_name='Unidad de Medida')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Fundo',
                'verbose_name_plural': 'Fundos',
                'ordering': ['name', 'location__name'],
            },
        ),
        migrations.CreateModel(
            name='PlantationDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_division', models.CharField(max_length=200, verbose_name='División Principal')),
                ('sub_division_1', models.CharField(blank=True, max_length=200, null=True, verbose_name='Sub División 1')),
                ('sub_division_2', models.CharField(blank=True, max_length=200, null=True, verbose_name='Sub División 2')),
                ('sub_division_3', models.CharField(blank=True, max_length=200, null=True, verbose_name='Sub División 3')),
                ('sub_division_4', models.CharField(blank=True, max_length=200, null=True, verbose_name='Sub División 4')),
                ('acronymo_note', models.CharField(max_length=30, verbose_name='Acrónimo')),
                ('acronymo_real', models.CharField(max_length=30, verbose_name='Acrónimo Real')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Fundo [Lote]',
                'verbose_name_plural': 'Fundos [Lotes]',
                'ordering': ['main_division', 'sub_division_1', 'sub_division_2'],
            },
        ),
        migrations.CreateModel(
            name='PlantationDivisionVariety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Cambio')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(blank=True, null=True, verbose_name='Fecha Modificación')),
            ],
            options={
                'verbose_name': 'Variedad [Lote]',
                'verbose_name_plural': 'Variedades [Lotes]',
                'ordering': ['plantation_division', 'crop_variety', 'created_date'],
            },
        ),
        migrations.CreateModel(
            name='PlantationDivisionVarietyTmp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_me', models.CharField(max_length=100, verbose_name='Unidad Medida')),
                ('variety', models.CharField(max_length=100, verbose_name='Variedad')),
                ('unit_me_equi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Unidad Medida Equi')),
                ('variety_equi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Variedad Equi')),
                ('plantation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='plantation_division_variety_temps', to='plantation.plantation')),
            ],
            options={
                'verbose_name_plural': 'plantationdivisionvariety_temps',
            },
        ),
    ]
