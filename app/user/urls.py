from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = "user"

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path('', include(router.urls)),
]
