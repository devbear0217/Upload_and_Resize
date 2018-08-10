from django import forms
from .models import ImageModel
from tempfile import NamedTemporaryFile
from django.core.files import File
from django.core.exceptions import ValidationError
import requests


class ImageForm(forms.ModelForm):

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        image_url = data['image_url']
        image_file = data['image_file']
        print(image_file)

        if not image_file and image_url:
            response = requests.get(image_url)
            content_type = response.headers['content-type']
            content_type = '.' + str(content_type.split('/')[1])
            image_temp = NamedTemporaryFile(delete=True)
            image_temp.write(requests.get(image_url).content)
            image_temp.flush()
            data['image_file'] = File(image_temp, 'image'+content_type)

        if image_file and image_url:
            raise ValidationError('Нельзя загрузить двумя методами одновременно. Пожалуйста, выберите один метод загрузки изображения')


        if not image_file and not image_url:
            raise ValidationError('Вы не можете отправить пустую форму')

    class Meta:
        model = ImageModel
        fields = ['image_file',
                  'image_url']
