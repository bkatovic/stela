# Generated by Django 3.1.7 on 2021-05-28 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stelaapp', '0013_auto_20210527_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]