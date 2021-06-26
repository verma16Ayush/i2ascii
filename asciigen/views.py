from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
from .forms import QueryForm
from .models import Query
from django.conf import settings
import os
from i2ascii.drive import *


def home(request:HttpRequest) -> HttpResponse:
    form = QueryForm()
    if(request.method == 'POST'):
        form = QueryForm(request.POST, request.FILES)
        if(form.is_valid()):
            form.save()
            last_entry = Query.objects.latest('id')
            img = last_entry.img.file.name
            out_img = convert_image_to_ascii(img)
            out_file_path = os.path.join(settings.MEDIA_ROOT, 'output.txt')
            f = open(out_file_path, 'w')
            for row in out_img:
                f.write(row + '\n')
            f.close()
            with open(out_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(out_file_path)
                return response
            # download(out_file_path)
    context = {'form':form}
    return render(request, 'index.html', context)


# def download(out_file_path):