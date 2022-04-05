# Generated by Django 3.1.3 on 2022-04-05 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220405_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='userRelated',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FileHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileRelativePath', models.TextField(verbose_name='filePath')),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('user_upd', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]