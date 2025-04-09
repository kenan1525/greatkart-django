# Generated by Django 5.1.7 on 2025-04-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_productgallery_options_product_anasayfa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Başlık')),
                ('description', models.TextField(blank=True, verbose_name='Açıklama')),
                ('image', models.ImageField(upload_to='slider_images/', verbose_name='Görsel')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Buton Linki')),
                ('order', models.IntegerField(default=0, verbose_name='Sıra Numarası')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
