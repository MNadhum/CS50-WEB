from django.urls import path
from . import views
from django.conf.urls import url

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.page, name="page"),
    path("wiki/", views.index, name="no_entry"),
    url(r'^search/$', views.search, name="search")
]

