from django.urls import path
from . import views

app_name="genel"
urlpatterns = [
    path("", views.home,name="home"),
    path("datasets/",views.dataset_list_sorted,name="datasets"),

]