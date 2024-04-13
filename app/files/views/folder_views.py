from rest_framework import views, response, serializers, permissions, authentication

from files.models import Folder, File
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model


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


class SharedWithMeView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        folders = Folder.objects.filter(shared_with=user)
        files = File.objects.filter(shared_with=user)

        return response.Response({
            'folders': FolderSerializer(folders, many=True).data,
            'files': FileSerializer(files, many=True).data
        })


class ShareFolderView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        folder_id = request.data.get('folder_id')
        shared_with_email = request.data.get('shared_with_email')

        try:
            folder = Folder.objects.get(user=user, id=folder_id)
        except Folder.DoesNotExist:
            return response.Response({'error': 'Folder not found'}, status=404)

        try:
            shared_with = get_user_model().objects.get(email=shared_with_email)
        except get_user_model().DoesNotExist:
            return response.Response({'error': 'User not found'}, status=404)

        folder.shared_with.add(shared_with)
        folder.save()

        folder.share_subfolders(shared_with)

        return response.Response({'message': 'Folder shared successfully'})
