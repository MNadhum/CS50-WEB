from django.urls import path
from . import views
from django.conf.urls import url

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.page, name="page"),
    path("wiki/", views.redirect, name="no_entry"),
    url(r'^search/$', views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("edit/", views.redirect, name="edit_no_entry"),
    path("random_page/", views.random_page, name="random_page")

]

