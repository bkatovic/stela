# Generated by Django 3.1.7 on 2021-06-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stelaapp', '0014_auto_20210528_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pesel',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
