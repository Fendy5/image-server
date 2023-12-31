# Generated by Django 4.2.4 on 2023-08-10 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=32, unique=True)),
                ('origin_name', models.CharField(max_length=512, null=True)),
                ('url', models.CharField(max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'img_images',
            },
        ),
    ]
