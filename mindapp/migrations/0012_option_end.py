# Generated by Django 2.1.5 on 2020-03-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindapp', '0011_auto_20200329_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='end',
            field=models.BooleanField(default=False),
        ),
    ]
