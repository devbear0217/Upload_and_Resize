from  django import forms


class ResizeForm(forms.Form):
    width_field = forms.IntegerField(required=True,
                                     label='Ширина',
                                     min_value=1)
    height_field = forms.IntegerField(required=True,
                                      label='Высота',
                                      min_value=1)
    size_field = forms.IntegerField(required=True,
                                    label='Размер изображения',
                                    min_value=1)
