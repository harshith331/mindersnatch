# Generated by Django 2.2.10 on 2021-08-12 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mindapp', '0072_auto_20210812_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situationtimer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mindapp.Player'),
        ),
    ]