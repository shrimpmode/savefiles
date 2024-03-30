from django.urls import path

from . import views

app_name = "user"


urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("delete/", views.DeleteUserView.as_view(), name="delete"),
]
