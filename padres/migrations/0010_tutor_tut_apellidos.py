# Generated by Django 2.0.1 on 2018-04-27 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('padres', '0009_auto_20180427_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='tut_apellidos',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
