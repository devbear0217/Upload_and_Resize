from django.shortcuts import render
from upload.models import ImageModel
# Create your views here.


def show_index_page(request):
    images = ImageModel.objects.all()
    return render(request, 'index.html', {'images': images})


