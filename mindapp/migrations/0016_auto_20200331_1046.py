# Generated by Django 2.1.4 on 2020-03-31 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mindapp', '0015_situation_ans'),
    ]

    operations = [
        migrations.RenameField(
            model_name='situation',
            old_name='next_level',
            new_name='next_sitn',
        ),
    ]