# Generated by Django 3.1.7 on 2021-05-23 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('interestId', models.IntegerField(primary_key=True, serialize=False)),
                ('interest', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('listId', models.IntegerField(primary_key=True, serialize=False)),
                ('listName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('universityid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('isCandidate', models.BooleanField(default=False)),
                ('studentIdNumber', models.CharField(max_length=11)),
                ('faculty', models.CharField(max_length=200)),
                ('DoB', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('university', models.ForeignKey(db_column='university', null=True, on_delete=django.db.models.deletion.CASCADE, to='stelaapp.university')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='cars')),
                ('aboutMe', models.CharField(max_length=500)),
                ('interestsId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stelaapp.interests')),
                ('listId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stelaapp.list')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
