from django.urls import path

from . import views

app_name = "post"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
]
