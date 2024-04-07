from rest_framework import views, response, serializers, permissions, authentication

from files.models import Folder, File
from rest_framework.decorators import permission_classes


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'


class FolderFilesViews(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, folder_id):
        user = request.user

        folders = Folder.objects.filter(
            user=user,
            parent__id=folder_id
        )
        files = File.objects.filter(user=user, parent__id=folder_id)

        return response.Response({
            'folders': FolderSerializer(folders, many=True).data,
            'files': FileSerializer(files, many=True).data
        })


