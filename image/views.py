import os
from io import BytesIO

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from ImageProject.settings import BASE_URL
from ImageProject.views import json_response, get_today
from image.models import ImageModel


# 上传图片
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        image_format, quality = request.POST.get('format', ''), request.POST.get('quality', 85)
        path = 'media/upload/images/' + get_today()
        image_urls = []  # 返回客户端的图片链接
        if not os.path.exists(path):
            os.makedirs(path)
        for i in files:
            image_id = get_random_string(32)
            suffix = i.name.split('.')[-1]
            if not image_format:
                image_format = suffix
            image_path = os.path.join(path, image_id + '.' + (suffix if suffix == 'svg' else image_format))
            # svg格式的图片另外处理
            if suffix == 'svg':
                with open(image_path, 'wb+') as destination:
                    for chunk in i.chunks():
                        destination.write(chunk)
            else:
                image = Image.open(BytesIO(i.read()))
                save_image(image_format, image, image_path, quality)
            image = ImageModel(image_id=image_id, origin_name=i.name, url=image_path, content_type=i.content_type)
            image.save()
            image_urls.append(f'{BASE_URL}/t/{image_id}')
        return json_response(image_urls, '上传成功')


# 根据图片的格式来保存图片
def save_image(image_format, image, path, quality):
    match image_format:
        case 'jpg':
            # 获取图像模式
            mode = image.mode
            # 判断图像是否为RGBA模式，如果是RGBA格式就转换为RGB格式
            if mode == "RGBA":
                image = image.convert("RGB")
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


def delete_image(request, image_id):
    return json_response(image_id)
