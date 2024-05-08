from dotenv import load_dotenv
import os
import pathlib
import re
import time
import json
import docx2txt
import shutil
import pandas as pd
from rest_framework import status
from pathlib import Path
from docx import Document
from datetime import datetime
from io import BytesIO
from PIL import Image
from file_manager.validations import validDate, validInt, validStrTest, countFiles, cleanAcronimo
from file_manager.constants import LABEL_NOTE_AGRI_VAR_LOTE, LABEL_NOTE_AGRI_VAR_DATE, LABEL_NOTE_AGRI_VAR_KIND, LABEL_NOTE_AGRI_VAR_DAYS, LABEL_NOTE_AGRI_VAR_DAYS_ACCENT, LABEL_NOTE_AGRI_VAR_TEST, LABEL_NOTE_AGRI_VAR_PRODUCT_APPLIED, LABEL_NOTE_AGRI_VAR_COMMENT
from background_task import background
from plantation.models import LandInfo, Land, Ndvi, Plantation, PlantationDivision, PlantationDivisionVariety
from django.db import transaction
from django.core.files import File
from django.contrib.auth import get_user_model
User = get_user_model()

from azure.storage.blob import BlobServiceClient

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials


class File_Manager():

    def upload_file(self, dir_target, file):
        try:
            Document(file)
            if file:
                os.makedirs(dir_target, exist_ok=True)
                output = os.path.join(dir_target, file.name)
                fn = open(output, 'wb+')
                for chunk in file.chunks():
                    fn.write(chunk)
                fn.close()

                file_size = Path(output).stat().st_size
                if file_size <= 11543:
                    raise ValueError(f"Ups! El archivo {file.name} esta vacio")

        except ValueError as err:
            raise ValueError(f"Ups! Formato errado del archivo {file.name} {err=}, {type(err)=}") from err
        except Exception as err:
            raise Exception(f"Ups! Algo salió mal cargando el archivo {file.name} {err=}, {type(err)=}") from err

    def delete_dir(self, dir_target):
        try:
            shutil.rmtree(dir_target)
        except OSError as err:
            raise ValueError(f"Ups! Algo salió mal borrando el directorio {dir_target} {err=}, {type(err)=}") from err

    @background()
    def runProcessBackground(dir_target, dir_out_cropped, dir_out_text, dir_out_json, file_name, dir_in, dir_id, dir_destiny_img, dir_out_img, current_dir, plantation_id, doc_kind, phase_crop, doc_comments, user):
        try:
            File_Manager.convert_word_to_imgs(dir_target, dir_destiny_img, file_name, dir_id)
            File_Manager.cropped_images(dir_target, dir_destiny_img, dir_out_img, dir_out_cropped)
            File_Manager.getTextRead(os.path.join(dir_target, dir_out_cropped), os.path.join(dir_target, dir_out_text))
            File_Manager.buildJsonRegister(os.path.join(dir_target, dir_out_text), os.path.join(dir_target, dir_out_json))
            File_Manager.create_blob(dir_in)
            File_Manager.upload_files_to_blob(dir_in, os.path.join(dir_target, file_name), file_name)
            File_Manager.insertNdvis(current_dir, dir_in, dir_out_json, dir_out_img, plantation_id, file_name, doc_kind, phase_crop, doc_comments, user)
        except Exception as err:
            raise Exception(f"Ups! Algo salió mal {err=}, {type(err)=}") from err

    @staticmethod
    def convert_word_to_imgs(dir_target, dir_destiny, file_name, dir_id):

        try:

            if os.path.isfile(os.path.join(dir_target, file_name),):
                os.makedirs(dir_destiny, exist_ok=True)
                docx2txt.process(os.path.join(dir_target, file_name), dir_destiny)

            initial_count = 0
            for path in pathlib.Path(dir_destiny).iterdir():
                if path.is_file():
                    initial_count += 1

            if initial_count == 0:
                raise Exception(f"Ups! Se extrajo 0 imagenes del archivo {file_name}")

            elif initial_count % 2 != 0:
                raise Exception(f"Ups! El archivo {file_name} contiene imagenes impares, recuerde cargar imagen recortada e imagen completa en ese orden")

            for filename in Path(dir_destiny).joinpath().glob('*.png'):
                num_img = filename.name[5:].split('.', 1)[0]
                os.rename(filename, os.path.join(dir_destiny, "image-" + str(num_img) + "-" + dir_id + ".png"))

            return {'total_images': num_img}, status.HTTP_200_OK

        except Exception as err:
            raise ValueError(f"Ups! Algo salió mal extrayendo las imagenes {err=}, {type(err)=}") from err

    @staticmethod
    def create_blob(dir_in):

        try:
            # Conecting to container
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create the container
            container_client = blob_service_client.get_container_client(dir_in)
            if not container_client.exists():
                container_client = blob_service_client.create_container(dir_in)

        except Exception as err:
            raise Exception(f"Ups! Algo salió mal creando el blob {err=}, {type(err)=}") from err

    @staticmethod
    def upload_files_to_blob(dir_in, upload_file_path, local_file_name):

        try:
            # Conecting to container
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=dir_in, blob=local_file_name)

            print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)

        except Exception as err:
            return {
                'error': f"Ups! Algo salió mal subiendo archivos al blob storage {err=}, {type(err)=}"
            }, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def cropped_images(dir_target, dir_destiny, dir_out_img, dir_out_cropped):
        cropped_images_paths = []
        cropped_images_list = []

        try:
            os.makedirs(os.path.join(dir_target, dir_out_cropped), exist_ok=True)

            if countFiles(dir_destiny) == 0:
                raise Exception(f"Ups! Ocurrio un error el directorio {dir_destiny} no tiene archivos")

            # Create an Image object from each image in a the Images folder.
            for image_path in Path(dir_destiny).joinpath().glob('*.png'):  # assume all images are png

                image = Image.open(image_path)
                w, h = image.size

                if w == 0 or h == 0:
                    raise Exception(f"Ups! El ancho o alto de la imagen no debe ser igual 0 en imagen {image_path.name}")
                elif w < 300:
                    raise Exception(f"Ups! El ancho es menor 300px en imagen {image_path.name}")
                elif h < 300:
                    raise Exception(f"Ups! El alto es menor 300px en imagen {image_path.name}")
                else:
                    num_img = int(image_path.name[6:].split('-', 2)[0])

                    # print(w, h)
                    if num_img % 2 == 0:
                        # edges: left, top, right, bottom+
                        img_cropped = image.crop((w - (w * 22 / 100), (h / 2) - 10, w, h - 50))
                        cropped = img_cropped.resize((1000, 1000))
                    else:
                        cropped = image
                    cropped_images_list.append(cropped)

                cropped_images_paths.append(pathlib.Path(str(image_path).replace(dir_out_img, dir_out_cropped)))
            for i in range(len(cropped_images_list)):
                # Convert cropped images back to PIL.JpegImagePlugin.JpegImageFile type
                b = BytesIO()

                cropped_images_list[i].save(b, format="png")
                cropped_images_list[i] = Image.open(b)
                # Save cropped image to file.
                cropped_images_list[i].save(cropped_images_paths[i], format="png", quality=100)
                b.close()

        except Exception as err:
            raise Exception(f"Ups! Algo salió mal cortando la imagen {err=}, {type(err)=}") from err

    @staticmethod
    def getTextRead(dir_target, path_dir_out_text):

        # Get Configuration Settings
        global cv_client
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Computer Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        try:

            os.makedirs(os.path.join(path_dir_out_text), exist_ok=True)

            if countFiles(dir_target) == 0:
                raise Exception(f"Ups! Ocurrio un error el directorio {dir_target} no tiene archivos")

            for image_file in Path(dir_target).joinpath().glob('*.png'):

                index_file = int(image_file.name[6:].split('-', 2)[0])

                if index_file % 2 == 0:
                    # print('Reading text in {}\n'.format(image_file))
                    file_names = os.path.split(image_file)

                    # Use Read API to read text in image
                    with open(image_file, mode="rb") as image_data:
                        read_op = cv_client.read_in_stream(image_data, raw=True)

                    # Get the async operation ID so we can check for the results
                    operation_location = read_op.headers["Operation-Location"]
                    operation_id = operation_location.split("/")[-1]

                    # Wait for the asynchronous operation to complete
                    while True:
                        read_results = cv_client.get_read_result(operation_id)
                        if read_results.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
                            break
                        time.sleep(1)

                    # If the operation was successfuly, process the text line by line
                    if read_results.status == OperationStatusCodes.succeeded:
                        f = open(os.path.join(path_dir_out_text, re.sub(".png$", "", file_names[-1]) + ".txt"), "w")
                        for page in read_results.analyze_result.read_results:
                            for line in page.lines:
                                # print(line.text)
                                f.write(line.text + "\n")

                    f.close()
        except Exception as err:
            raise Exception(f"Ups! Algo salió mal extrayendo el texto de la imagen {file_names} {err=}, {type(err)=}") from err

    @staticmethod
    def convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    @staticmethod
    def buildNvdiDt(text_path, i):
        # initialize dataframe.
        #COLOR_CHOICES = (
        #    ('1', 'Verde'),
        #    ('2', 'Amarillo'),
        #    ('3', 'Anaranjado'),
        #    ('4', 'Anaranjado Oscuro'),
        #    ('5', 'Rojo'),
        #)
        #CLASE_CHOICES = (
        #    ('1', 'Muy Bueno'),
        #    ('2', 'Bueno'),
        #    ('3', 'Regular'),
        #    ('4', 'Deficitario'),
        #    ('5', 'Muy Deficitario'),
        #)
        data_desc = pd.DataFrame.from_dict({'color': ['1', '2', '3', '4', '5'],
                                            'type': ['1', '2', '3', '4', '5'],
                                            })

        try:
            file = open(text_path)
            exist = False
            cont = 0
            list_min = []
            list_max = []
            list_ha = []
            list_area = []

            for line in file.readlines():
                if exist:
                    len_decimals = len(line.replace(',', '.').split('.')[-1]) - 1
                    if len_decimals < 2:
                        raise Exception(f"Ups! Algo salió mal el registro no tiene un formato númerico de dos decimales {line} en el archivo {file.name}")
                    line_ft = float(line.replace(',', '.'))
                    if isinstance(line_ft, (float)):
                        if cont < 4:

                            if cont == 0:
                                list_min.append(line_ft)

                            if cont == 1:
                                list_max.append(line_ft)

                            if cont == 2:
                                list_ha.append(line_ft)

                            if cont == 3:
                                list_area.append(line_ft)

                            cont = cont + 1

                        if cont == 4:
                            cont = 0
                    else:
                        raise Exception(f"Ups! Algo salió mal el registro no tiene un formato númerico {file.name}, número {line_ft}")

                if line.find("%") != -1:
                    exist = True

                if len(list_min) == 5 and len(list_max) == 5 and len(list_ha) == 5 and len(list_area) == 5:
                    break

            data_desc.insert(2, 'min', pd.Series(list_min))
            data_desc.insert(3, 'max', pd.Series(list_max))
            data_desc.insert(4, 'ha', pd.Series(list_ha))
            data_desc.insert(5, 'area', pd.Series(list_area))

            dict_t = data_desc.to_dict(orient='records')
            return json.dumps(dict_t)
        except Exception as err:
            raise Exception(f"Ups! Algo salió mal construyendo el mapa de indices de vegetación {err=}, {type(err)=}") from err

    @staticmethod
    def buildJsonRegister(dir_target, path_dir_out_json):
        dict_data = {}

        try:
            os.makedirs(os.path.join(path_dir_out_json), exist_ok=True)

            if countFiles(dir_target) == 0:
                raise Exception(f"Ups! Ocurrio un error el directorio {dir_target} no tiene archivos")

            for i, text_path in enumerate(Path(dir_target).joinpath().glob('*.txt')):

                file = open(text_path)
                exist = False
                list_data = []

                for index, line in enumerate(file.readlines()):

                    line_lower = line.lower()

                    if exist:
                        if line_lower.find(LABEL_NOTE_AGRI_VAR_DATE) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_KIND) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_DAYS) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_DAYS_ACCENT) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_TEST) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_PRODUCT_APPLIED) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_COMMENT) != -1:

                            ind_cut = line.find(':')
                            value = line[ind_cut + 1:]

                            try:
                                if line_lower.find(LABEL_NOTE_AGRI_VAR_KIND) != -1:
                                    list_data.append("kind")
                                    list_data.append(value.strip())

                                elif line_lower.find(LABEL_NOTE_AGRI_VAR_TEST) != -1:
                                    list_data.append("test")
                                    list_data.append(validStrTest(value.strip()))

                                elif line_lower.find(LABEL_NOTE_AGRI_VAR_DATE) != -1:
                                    list_data.append("date")
                                    list_data.append(validDate(value.strip()))

                                elif line_lower.find(LABEL_NOTE_AGRI_VAR_DAYS) != -1 or line_lower.find(LABEL_NOTE_AGRI_VAR_DAYS_ACCENT) != -1:
                                    list_data.append("days")
                                    list_data.append(validInt(value.strip()))

                                elif line_lower.find(LABEL_NOTE_AGRI_VAR_PRODUCT_APPLIED) != -1:
                                    list_data.append("pa")
                                    list_data.append(value.strip())

                                elif line_lower.find(LABEL_NOTE_AGRI_VAR_COMMENT) != -1:
                                    list_data.append("comments")
                                    list_data.append(value.strip())
                            except Exception as err:
                                raise Exception(f"Ups! Algo salió mal validando los datos {err=}, {type(err)=}")

                    if line_lower.find(LABEL_NOTE_AGRI_VAR_LOTE) != -1:
                        ind_cut = line.find(':')
                        value = line[ind_cut + 1:]
                        list_data.append("umt")
                        listOfChars = list(value)
                        if listOfChars[1] == '1':
                            listOfChars[1] = 'i'
                            list_data.append(''.join(listOfChars).strip())
                        else:
                            list_data.append(value.strip())
                        exist = True

                    if line_lower.find(LABEL_NOTE_AGRI_VAR_COMMENT) != -1:
                        break

                    # else:
                    #    raise Exception(f"Ups! La etiqueta de la nota no cumple con el formato ruta archivo: {text_path} linea: {line} número de linea: {index}")

                file_names = os.path.split(text_path)

                # Get name origin file
                split_name_file = re.sub(".txt$", "", file_names[-1]) .split('-', 2)
                index_file = int(split_name_file[1]) - 1
                split_name_file[1] = "-" + str(index_file) + "-"
                joined_string = "".join(split_name_file)

                dict_data = File_Manager.convert(list_data)
                dict_data["name_img"] = joined_string + ".png"
                dict_data["ndvi"] = File_Manager.buildNvdiDt(text_path, i)
                # print(dict_data)

                with open(os.path.join(path_dir_out_json, re.sub(".txt$", "", file_names[-1]) + ".json"), 'w') as f:
                    js = json.dumps(dict_data, indent=4)
                    js = js.replace('\\', '').replace('"[', '[').replace(']"', ']')
                    f.write(js)
                    f.close()
                file.close()
        except Exception as err:
            raise Exception(f"Ups! Algo salió mal construyendo el registro {err=}, {type(err)=}") from err

    @staticmethod
    def insertNdvis(current_dir, dir_in, dir_out_json, dir_out_img, plantation_id, doc_name, doc_kind, phase_crop, doc_comments, user):
        try:
            with transaction.atomic():
                dir_target = os.path.join(current_dir, dir_in, dir_out_json)

                land_info = LandInfo(plantation=Plantation.objects.get(id=plantation_id),
                                doc_name=doc_name,
                                doc_kind=doc_kind,
                                phase_crop=phase_crop,
                                comments=doc_comments,
                                created_by_id=user
                                )
                land_info.save()
               
                read_flight = False
                flight_num = 0
                for i, filename in enumerate(Path(dir_target).joinpath().glob('*.json')):
                    # Opening JSON file
                    file_json = open(filename)
                    data = json.load(file_json)

                    try:
                        if data['umt']:
                            umt = cleanAcronimo(str(data['umt']).strip())
                            plantation_division = PlantationDivision.objects.get(acronymo_real=umt, plantation_id=plantation_id)
                    except Exception as err:
                        raise Exception(f"El acronimo {umt} no existe para el fundo con id {plantation_id} por favor revise que se encuentre bien escrito en el archivo {file_json.name} o que este creado en el sistema") from err

                    try:
                        plantation_division_var_id = PlantationDivisionVariety.objects.filter(plantation_division_id=plantation_division.id).order_by('created_date').values('id')[0]['id']
                    except Exception as err:
                        raise Exception(f"No se tiene variedad asociada en el archivo {file_json.name}, por favor creela")  from err

                    if data['kind']:
                        kind = str(data['kind']).upper()
                        if kind != 'DDC' and kind != 'DDP' and kind != 'DDS':
                            raise Exception(f"El tipo de tratamiento {kind} no esta definido en el archivo {file_json.name}, recuerde que solo se admite DDP, DDC ó DDS")

                    product_applied = ''
                    if 'pa' in data:
                        product_applied = data['pa']

                    test = str(data['test']).upper()
                    bool_test = False
                    if test == 'T':
                        bool_test = True

                    last_land = Land.objects.select_related('land_info').filter(land_info__plantation_id=plantation_id, land_info__phase_crop=phase_crop, is_test=False, land_info__doc_kind='1', date__year=datetime.strptime(data['date'], '%d/%m/%Y').year).order_by('-date')

                    if read_flight is False:
                        if last_land.exists():
                            flight_num = last_land[0].flight_number + 1
                        else:
                            flight_num = 1
                        read_flight = True

                    land = Land(plantation_division_variety=PlantationDivisionVariety.objects.get(id=plantation_division_var_id),
                                date=datetime.strptime(data['date'], '%d/%m/%Y'),
                                kind_proccess=kind,
                                days_process=data['days'],
                                comments=data['comments'],
                                is_test=bool_test,
                                applied_product=product_applied,
                                land_info=land_info,
                                json_name=file_json.name,
                                created_by_id=user,
                                )

                    if doc_kind == '1':
                        land.flight_number = flight_num
                        land.save()

                    if os.getenv('DEBUG_MODE') == "False":
                        url_external_img = os.getenv('AZURE_BLOB_STORAGE_URL_MEDIA') + 'images/' + data['name_img']
                    else:
                        url_external_img = 'media/images/' + data['name_img']

                    land.url_external = url_external_img

                    path = Path(os.path.join(current_dir, dir_in, dir_out_img, data['name_img']))
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
                                        land=land,
                                        created_by_id=user,
                                        )
                            ndvi.save()
        except Exception as err:
            raise Exception(f"Ups, hubo un error cargando los datos del archivo {file_json.name}") from err
