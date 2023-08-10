from django.db import models


# 图片信息表
class ImageModel(models.Model):
    class Meta:
        db_table = 'img_images'

    image_id = models.CharField(max_length=32, unique=True)
    origin_name = models.CharField(max_length=512, null=True)  # 图片的原始名字
    content_type = models.CharField(max_length=32, null=True)  # 图片类型
    url = models.CharField(max_length=128, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin_name
