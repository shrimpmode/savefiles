from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import folder_views
router = DefaultRouter()

print('test')

urlpatterns = [
    path('folder/<int:folder_id>/content/', folder_views.FolderFilesViews.as_view(), name='folder_files'),
    path('shared-with-me/', folder_views.SharedWithMeView.as_view(), name='shared_with_me'),
    path('share-folder/', folder_views.ShareFolderView.as_view(), name='share_folder'),
    path('', include(router.urls)),
]