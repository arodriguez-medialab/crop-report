import json
import os
from pathlib import Path
from django.db import transaction
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from plantation.models import Land, Ndvi, Plantation,  PlantationDivision, Client, PlantationDivisionVarietyTmp, LandTmp, NdviTmp, PlantationDivisionVariety, LandInfo, DocPhaseTmp
from datetime import datetime


class LoadNdvisView(APIView):
    def post(self, request, format=None):
        dir_name = '20220317-docs-1c36c03b-b9a0-4f7f-a381-107d57ee1964'
        dir_out_json = "json-text-files"
        dir_out_img = "img"
        data = self.request.data

        try:
            plantation_id = int(data['plantation_id'])
            flight_number = int(data['flight_number'])
            dir_name = data['dir_name']
            #flight_date = date(data['flight_date'])
        except Exception:
            return Response({'error': 'El ID del fundo debe ser un entero'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                current_dir = os.getcwd()
                dir_target = os.path.join(current_dir, dir_name, dir_out_json)

                for i, filename in enumerate(Path(dir_target).joinpath().glob('*.json')):
                    # Opening JSON file
                    f = open(filename)
                    data = json.load(f)

                    try:
                        if data['umt']:
                            umt = str(data['umt']).strip()
                            plantation_division = PlantationDivision.objects.get(acronymo_note=umt, plantation_id=plantation_id)
                    except Exception:
                        raise Exception(f"El acronimo no existe por favor revise que se encuentre bien escrito en el archivo {f.name} o que este creado en el sistema")

                    try:
                        plantation_division_variety_id = PlantationDivisionVariety.objects.filter(plantation_division_id=plantation_division.id).order_by('created_date').values('id')[0]['id']
                    except Exception:
                        raise Exception(f"No se tiene variedad asociada en el archivo {f.name}, por favor creela")

                    if data['kind']:
                        kind = str(data['kind']).upper()
                        if kind != 'DDC' and kind != 'DDP' and kind != 'DDS':
                            raise Exception(f"El tipo de tratamiento {kind} no esta definido en el archivo {f.name}, recuerde que solo se admite DDP, DDC ó DDS")

                    test = str(data['test']).upper()
                    bool_test = True
                    if test != 'T' or test != '':
                        raise Exception(f"El tipo de tratamiento {test} no esta definido en el archivo {f.name}, recuerde que solo se admite T si es testigo")
                    else:
                        bool_test = True

                    land = Land(plantation_division_variety=PlantationDivisionVariety.objects.get(id=plantation_division_variety_id),
                                date=datetime.strptime(data['date'], '%d/%m/%Y'),
                                kind_proccess=kind,
                                days_process=data['days'],
                                comments=data['comments'],
                                is_test=bool_test,
                                applied_product=data['pa'],
                                flight_number=flight_number
                                )

                    path = Path(os.path.join(current_dir, dir_name, dir_out_img, data['name_img']))
                    with path.open(mode='rb') as f:
                        land.url_image = File(f, name=path.name)
                        land.save()

                        for item in data['ndvi']:
                            ndvi = Ndvi(color=item['color'],
                                        clase=item['type'],
                                        min=item['min'],
                                        max=item['max'],
                                        ha=item['ha'],
                                        area=item['area'],
                                        land=land
                                        )
                            ndvi.save()

            return Response({'success': f'El archivo {f.name} fue cargado correctamente'}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': f"Ups, hubo un error cargando los datos {err=}, {type(err)=}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoadHistoricalView(APIView):
    def post(self, request):
        uid = '02b31687-b849-4a7f-aec2-d2b8db251747'
        dir_name = '20220317-docs-1c36c03b-b9a0-4f7f-a381-107d57ee1964'
        dir_out_json = "json-text-files"
        bool_test = False
        data_request = request.data
    
        try:
            image_file = data_request.pop('image')[0]
            data = json.load(data_request.pop('json_file')[0])
            json_name = data_request.pop('json_name')[0]

            try:
                flight_number = int(data['flight_number'])
            except:
                return Response({'error': 'El Numero de Vuelo debe ser un entero'}, status=status.HTTP_404_NOT_FOUND)


            with transaction.atomic():
                try: 
                    if data['company'] and data['umt'] and data['fundo']:
                        company = str(data['company']).strip()
                        # umt = str(data['umt']).strip()
                        fundo = str(data['fundo']).strip()
                        cliente = Client.objects.get(name__iexact = company)
                        plantation = Plantation.objects.get(name__iexact = fundo, client__id = cliente.id)
                except Client.DoesNotExist:
                    content = {"Error": "Cliente no existe."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                except Plantation.DoesNotExist:
                    content = {"Error": "La Plantacion no existe."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                try:
                    plantation_division_variety_tmp = PlantationDivisionVarietyTmp.objects.get(
                        unit_me__iexact = data['unid'],
                        variety__iexact = data['var'],
                        plantation = plantation)
                except PlantationDivisionVarietyTmp.DoesNotExist:
                    plantation_division_variety_tmp = PlantationDivisionVarietyTmp(
                        unit_me = data['unid'],
                        variety = data['var'],
                        plantation = plantation)
                    plantation_division_variety_tmp.save()
                        
                if data['kind']:
                    kind = str(data['kind']).upper()
                    if kind != 'DDC' and kind != 'DDP' and kind != 'DDS' and kind != 'DDD':
                        content = {"Error": f"El tipo de tratamiento {kind} no esta definido, recuerde que solo se admite DDP, DDC ó DDS"}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)

                if data['test'] and str(data['test']).upper() == 'T' :
                    bool_test = True
                    
                land_tmp = LandTmp(
                    plantation_division_variety_tmp = plantation_division_variety_tmp,
                    date = datetime.strptime(data['date'], '%d/%m/%Y'),
                    kind_proccess = kind,
                    days_process = data['days'],
                    comments = data['comments'],
                    is_test = bool_test,
                    applied_product= data['pa'],
                    flight_number = flight_number,
                    url_image = image_file,
                    total_area = float(data['total_hectare']),
                    doc_name = data['doc_name'],
                    json_name = json_name
                    )

                # print('total_hectare', float(data['total_hectare']))
                # print('doc_name', data['doc_name'])
                # print('json_name', json_name)
                
                # land_tmp.url_image = image_file
                # land_tmp.url_image = File(image_file, name=image_file.name +'_' +str(uuid4()))
                land_tmp.save()


                for nvdi in list(data["ndvi"]):
                    Ndvi_tmp = NdviTmp(
                        color=nvdi['color'], 
                        clase=nvdi['type'], 
                        min=float(nvdi['min']), 
                        max=float(nvdi['max']), 
                        ha=float(nvdi['ha']), 
                        area=float(nvdi['area']), 
                        land_tmp=land_tmp )
                    Ndvi_tmp.save()
        

                
                # if os.getenv('FILES_DIR') == 'AZURE':
                #     pass
                #     # BASE_DIR_FILES = os.path.join(Path(__file__).resolve().parent.parent.parent.parent, "home/site/wwwroot/infolab_files/{}/".format(type))
                # else:
                #     BASE_DIR_FILES = 'images_files/'
                
                # file_id = str(uuid4())
                # date_name = str(datetime.now().strftime("%Y%m%d")) 
                # file_name = BASE_DIR_FILES + str(date_name) + '_' + '_' + str(file_id) + '_' + str(data['name_img'])
                # if not os.path.exists(BASE_DIR_FILES):
                #     os.makedirs(BASE_DIR_FILES)
                # with open(file_name, 'wb+') as destination:
                #     for chunk in image_file.chunks():
                #         destination.write(chunk)

            return Response({'success': f'La Informacion fue cargado correctamente'}, status=status.HTTP_200_OK)
            
            
        except Exception as err:
            return Response({'error': f"Ups, hubo un error cargando los datos {err=}, {type(err)=}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoadHistoricalTmpView(APIView):
    def get(self, request):
        try:
            
            with transaction.atomic():
                print('entro')
                id_plantation = 4
                # doc_name = 'INFORME 1_Agrolatina'
                # doc_name = 'Informe_Procesos Agroindustriales_Fundo Qolca_2V'
                # doc_name = 'APROA PRODUCCIÓN 2021_EDITADO'
                doc_name = '6V SANTAROSA PROD 2021'
                
                plantation = Plantation.objects.get(pk = id_plantation)
                # usuario = User.objects.get(pk = 2)
                plantation_division_variety_tmps = PlantationDivisionVarietyTmp.objects.filter(plantation = plantation)
                print('TRAZA 0')
                for tmp in plantation_division_variety_tmps:
                    # print(tmp.unit_me_equi)
                    # print(tmp.plantation)
                    # print(tmp.unit_me_equi)
                    
                    try:
                        plantation_division = PlantationDivision.objects.get(plantation = plantation, acronymo_note__iexact = tmp.unit_me_equi)
                        print('TRAZA 0-1')
                        print('TRAZA 0-1 plantation', plantation.id)
                        print('TRAZA 0-1 plantation_division', plantation_division.id)
                        print('TRAZA 0-1 tmp.unit_me_equi', tmp.unit_me_equi)
                        print('TRAZA 0-1 tmp.variety_equi', tmp.variety_equi)
                        print('TRAZA 0-1 tmp.unit_me', tmp.unit_me)
                        print('TRAZA 0-1 tmp.unit_me', tmp.id)
                        plantation_division_variety = PlantationDivisionVariety.objects.get(plantation_division = plantation_division, crop_variety__name__iexact = tmp.variety_equi)
                    except Exception:
                        raise Exception(f"La exception esta en {plantation_division.id} , {tmp.variety} , {tmp.unit_me}, {tmp.variety_equi}, {tmp.unit_me_equi}")

                    print('TRAZA 0-1')
                    land_tmps = LandTmp.objects.filter(plantation_division_variety_tmp = tmp, doc_name = doc_name)
                    
                    for land_tmp in land_tmps:
                        print(land_tmp.kind_proccess)
                        print(land_tmp.days_process)
                        print(land_tmp.doc_name)
                        
                        
                        doc_phase_tmp = DocPhaseTmp.objects.get(doc_name__iexact = land_tmp.doc_name)
                        if doc_phase_tmp.phase_is:
                            phase_crop_dsc = str(doc_phase_tmp.phase_is)
                        else:
                            phase_crop_dsc = None
                            
                        try:
                            land_info = LandInfo.objects.get(
                                plantation = plantation,
                                flight_number = land_tmp.flight_number,
                                doc_name = land_tmp.doc_name,
                                file = 'NO HAY.docx',
                                doc_kind = 1,
                                phase_crop = phase_crop_dsc
                                )
                            
                        except LandInfo.DoesNotExist:
                            land_info = LandInfo(
                                plantation = plantation,
                                flight_number = land_tmp.flight_number,
                                doc_name = land_tmp.doc_name,
                                file = 'NO HAY.docx',
                                doc_kind = 1,
                                phase_crop = phase_crop_dsc,
                                created_by_id = 2
                            )
                            print('INICIO TRAZA 0-1')
                            print('plantation:', plantation)
                            print('flight_number:' , land_tmp.flight_number)
                            print('doc_name:' , land_tmp.doc_name)
                            print('phase_crop:' , phase_crop_dsc)
                            print('FINAL TRAZA 0-1')
                            land_info.save()
                        print('TRAZA 1')
                        
                        
                        land = Land(
                            plantation_division_variety = plantation_division_variety,
                            date = land_tmp.date,
                            kind_proccess = land_tmp.kind_proccess,
                            days_process = land_tmp.days_process,
                            comments = land_tmp.comments,
                            is_test = False,
                            applied_product = land_tmp.applied_product,
                            url_image = land_tmp.url_image,
                            url_external = land_tmp.url_image.name.replace('images','https://agritopstorage.blob.core.windows.net/media/images'),
                            json_name = land_tmp.json_name,
                            land_info = land_info,
                            created_by_id = 2
                            )
                        
                        # # if os.getenv('DEBUG_MODE') == "False":
                        # #     url_external_img = os.getenv('AZURE_BLOB_STORAGE_URL_MEDIA') +'/' +land_tmp.url_image.name
                        # # else:
                        # #     url_external_img = 'media/' + land_tmp.url_image.name
                        # # land.url_external = url_external_img
                        land.save()
                        print('TRAZA 2')
            
                        ndvi_tmps = NdviTmp.objects.filter(land_tmp = land_tmp)
                        for ndvi_tmp in ndvi_tmps:
                            
                            if ndvi_tmp.color == 'Verde' : 
                                color_id = '1'
                            elif ndvi_tmp.color == 'Amarillo' : 
                                color_id = '2'
                            elif ndvi_tmp.color == 'Anaranjado' : 
                                color_id = '3'
                            elif ndvi_tmp.color == 'Anaranjado Oscuro' : 
                                color_id = '4'
                            elif ndvi_tmp.color == 'Rojo' : 
                                color_id = '5'
                            
                            
                            ndvi = Ndvi(
                                color=color_id, 
                                clase=color_id, 
                                min=ndvi_tmp.min, 
                                max=ndvi_tmp.max, 
                                ha=ndvi_tmp.ha, 
                                area=ndvi_tmp.area, 
                                land=land,
                                created_by_id = 2)
                            ndvi.save()
                        print('TRAZA 3')
                return Response({'success': f'La Informacion fue cargado correctamente'}, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({'error': f"Ups, hubo un error cargando los datos {err=}, {type(err)=}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
