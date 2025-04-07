# Generated by Django 5.1.7 on 2025-04-06 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productgallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'productgallery', 'verbose_name_plural': 'product gallery'},
        ),
        migrations.AddField(
            model_name='product',
            name='anasayfa',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='seo_title',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
    ]
