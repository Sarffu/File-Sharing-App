import shutil
# from numpy import require
from rest_framework import serializers
from .models import *


class FileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Files
        fields = '__all__'

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000 , allow_empty_file = False , use_url = False)
    )
    folder = serializers.CharField(required = False)
    
    def zip_files(self,folder):
        shutil.make_archive(f'public/static/zip/{folder}' , 'zip' ,f'public/static/{folder}' )
    
    def create(self, validated_data):
        folder = Folder.objects.create()
        folder_uid = str(folder.uid)
        folder_path = f'public/static/{folder_uid}'

    
        os.makedirs(folder_path, exist_ok=True)

        files = validated_data.pop('files')
        file_objs = []

        for file in files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            
            file_obj = Files.objects.create(folder=folder, file=f'static/{folder_uid}/{file.name}')
            file_objs.append(file_obj)

        self.zip_files(folder_uid)

        return {'files': {}, 'folder': folder_uid}
