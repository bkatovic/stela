# Generated by Django 3.1.7 on 2021-05-27 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stelaapp', '0008_auto_20210527_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
