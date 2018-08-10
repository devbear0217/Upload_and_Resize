from django.urls import path
from . import views

urlpatterns = [
    path('upload/',
         views.image_form_upload,
         name='upload_page')
]