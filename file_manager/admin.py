from django.contrib import admin
import os
import pathlib
from uuid import uuid4
import logging
from plantation.models import LandInfo
from datetime import datetime
from django.contrib import messages

from file_manager.filemanager import File_Manager

@admin.register(LandInfo)
class LandInfoAdmin(admin.ModelAdmin):
    list_display = ["plantation", "doc_name", "doc_kind", "phase_crop", 'created_by', 'created_date', 'modified_by', 'modified_date']
    ordering = ['plantation']
    list_filter = ('plantation', 'doc_kind', 'phase_crop', )
    exclude = ['doc_name', 'created_by', 'modified_by', 'created_date', 'modified_date']

    def save_model(self, request, obj, form, change):
        if request.method == "POST":
            if obj.file:
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
                obj_file = File_Manager()
                obj_file.upload_file(dir_target, obj.file)
                obj_file.runProcessBackground(
                                            dir_target,
                                            dir_out_cropped,
                                            dir_out_text,
                                            dir_out_json,
                                            obj.file.name,
                                            dir_in,
                                            dir_id,
                                            dir_destiny_img,
                                            dir_out_img,
                                            main_dir,
                                            obj.plantation.id,
                                            obj.doc_kind,
                                            obj.phase_crop,
                                            obj.comments,
                                            request.user.id
                                            )

                messages.add_message(request, messages.INFO, f'El tiempo de carga del archivo {obj.file.name} dependerá del tamaño del mismo, nombre del directorio {dir_in}')

    def has_change_permission(self, request, obj=None):
        return False

    ##def save_model(self, request, obj, form, change):
    ##    if obj.pk is None:
    ##        obj.created_by = request.user
    ##        obj.created_date = datetime.now()
    ##    else:
    ##        obj.modified_by = request.user
    ##        obj.modified_date = datetime.now()

    ##    super().save_model(request, obj, form, change)