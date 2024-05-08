import os
import pathlib
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
from datetime import datetime

from file_manager.filemanager import File_Manager

# Create your views here.
class LoadNdviFileView(APIView):
    def post(self, request, format='docx'):
        file = request.data["file"]

        try:
            plantation_id = int(request.data['plantation_id'])
            flight_number = int(request.data['flight_number'])
            doc_kind = request.data['doc_kind']
            phase_crop = request.data['phase_crop']
            doc_comments = request.data['comments']
            #flight_date = date(data['flight_date'])
        except Exception:
            return Response({'error': 'El ID del fundo debe ser un entero'}, status=status.HTTP_404_NOT_FOUND)

        if file:
            if os.getenv('DEBUG_MODE') == "False":
                main_dir = os.getenv('DIR_HOME_WWWROOT_DOCS')
            else:
                main_dir = os.getcwd()

            dir_id = str(uuid4())
            dir_date_name = str(datetime.now().strftime("%Y%m%d"))
            dir_in = dir_date_name + "-" + "docs-" + dir_id
            dir_out_img = "img"
            dir_out_cropped = "cropped-images"
            dir_out_text = "ocr-text-files"
            dir_out_json = "json-text-files"
            dir_target = os.path.join(main_dir, dir_in)
            dir_destiny_img = os.path.join(dir_target, dir_out_img)
            working_directory = pathlib.Path(os.path.dirname(__file__))

            logging.basicConfig(filename='myapp.log', level=logging.INFO)

            logging.info('Current Path--' + main_dir)
            logging.info('Directory Target--' + dir_target)
            logging.info('Directory Destiny Images--' + dir_out_img)
            logging.info('Directory Destiny Images Cropped--' + dir_out_cropped)
            logging.info('Directory Destiny Text Ocr--' + dir_out_cropped)
            logging.info('Working Destiny--' + str(working_directory))

            try:
                obj_file = File_Manager()
                obj_file.upload_file(dir_target, file)
                obj_file.runProcessBackground(
                                            dir_target,
                                            dir_out_cropped,
                                            dir_out_text,
                                            dir_out_json,
                                            file.name,
                                            dir_in,
                                            dir_id,
                                            dir_destiny_img,
                                            dir_out_img,
                                            main_dir,
                                            plantation_id,
                                            flight_number,
                                            doc_kind,
                                            phase_crop,
                                            doc_comments,
                                            request.user.id
                                            )
            except ValueError as err:
                return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
            # finally:
            #    delete_dir(dir_target)

            return Response({'success': f'El tiempo de carga del archivo {file.name} dependerá del tamaño del mismo', 'directory': dir_in}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f'Ups, el archivo {file.name} no fue leido correctamente'}, status=status.HTTP_400_BAD_REQUEST)