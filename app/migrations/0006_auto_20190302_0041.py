# Generated by Django 2.1.2 on 2019-03-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190302_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfav',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]