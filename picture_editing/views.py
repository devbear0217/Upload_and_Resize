from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from upload.models import ImageModel
from .forms import ResizeForm
from django.conf import settings
import os
import io
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
# Create your views here.


def edit_image(request, pk):
    image = get_object_or_404(ImageModel, pk=pk)
    query_params = request.GET.getlist('query_params', default=[''])
    if query_params[0].isdigit and query_params != ['']:
        query_params = [x.split(',') for x in query_params]
        query_params = [j for sub in query_params for j in sub]
    if request.method == 'POST':
        resize_form = ResizeForm(request.POST)
        if resize_form.is_valid:
            width = request.POST.get('width_field')
            height = request.POST.get('width_field')
            size = request.POST.get('size_field')
            tmp_path = 'tmp/%s' % image.image_file.name
            default_storage.save(tmp_path, ContentFile(image.image_file.read()))
            full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
            img_file = io.StringIO(full_tmp_path)
            img = Image.open(img_file.read())
            img = img.resize((int(width), int(height)), Image.ANTIALIAS)
            img.save(full_tmp_path)
            if os.path.getsize(full_tmp_path) > int(size):
                raise ValidationError('Размеры файла превышают заданный размер изображения. Пожалуйста, напишите значения ширины и высоты поменьше')
            if os.path.exists(full_tmp_path):
                with open(full_tmp_path, 'rb') as fh:
                    fh = fh.read()
                    response = HttpResponse(fh, content_type='application/force-download')
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(full_tmp_path)
                    default_storage.delete(tmp_path)
                    return response
    else:
        resize_form = ResizeForm()
    return render(request, 'image.html', {'image': image,
                                          'resize_form': resize_form,
                                          'query_params': query_params})
