# Generated by Django 3.2.5 on 2021-07-04 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20210704_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=16),
        ),
    ]
