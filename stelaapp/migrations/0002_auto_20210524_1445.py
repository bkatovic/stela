# Generated by Django 3.1.7 on 2021-05-24 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stelaapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote_record',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stelaapp.candidate'),
        ),
        migrations.AlterField(
            model_name='vote_record',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
