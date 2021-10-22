from django.urls import  path
from . import views


urlpatterns = [
    path('', views.index, name="index"), 
    path('status/', views.status, name="status"),
    path('download/<int:job>/', views.download, name="download")
]