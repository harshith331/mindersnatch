# Generated by Django 2.2.10 on 2021-08-09 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mindapp', '0061_auto_20210809_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situationtimer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mindapp.Player'),
        ),
    ]
