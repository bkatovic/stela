# Generated by Django 3.1.7 on 2021-05-23 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stelaapp', '0003_auto_20210523_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='solutions',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]