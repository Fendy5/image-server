import os
from io import BytesIO

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from ImageProject.views import json_response, get_today
from image.models import ImageModel


# 上传图片
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        image_format, quality = request.POST.get('format'), request.POST.get('quality')
        path = 'media/upload/images/' + get_today()
        if not os.path.exists(path):
            os.makedirs(path)
        for i in files:
            suffix = i.name.split('.')[-1]
            image_id = get_random_string(32)
            image_path = os.path.join(path, image_id + '.' + (suffix if suffix == 'svg' else image_format))
            if suffix == 'svg':
                with open(image_path, 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
            else:
                image = Image.open(BytesIO(i.read()))
                save_image(image_format, image, image_path, quality)
            image = ImageModel(image_id=image_id, origin_name=i.name, url=image_path, type=i.content_type)
            image.save()
    return json_response('', '上传成功')


def save_image(image_format, image, path, quality):
    match image_format:
        case 'jpg':
            image.save(path, format='JPEG', quality=int(quality))
        case 'png':
            image.save(path, format='PNG', optimize=True)
        case 'webp':
            image.save(path, format='WebP', lossless=True)


# 获取图片
def get_image(request, image_id):
    image = get_object_or_404(ImageModel, image_id=image_id)
    image_path = image.url
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type=image.content_type)


def delete_image():
    return json_response('delete_image')
