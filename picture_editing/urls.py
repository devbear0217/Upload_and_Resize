from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/',
         views.edit_image,
         name='image_page')
]
