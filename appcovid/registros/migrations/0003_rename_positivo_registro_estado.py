# Generated by Django 3.2 on 2021-04-13 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_alter_registro_positivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registro',
            old_name='positivo',
            new_name='estado',
        ),
    ]
