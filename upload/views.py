from django.shortcuts import render, redirect
from .forms import ImageForm
# Create your views here.


def show_upload_page(request):
    return render(request, 'upload.html')


def image_form_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_page')
    else:
        form = ImageForm
    return render(request, 'upload.html', {'form': form})
