# Generated by Django 3.1.3 on 2022-04-05 05:49

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220405_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static', validators=[api.validators.FileValidator()]),
        ),
    ]
