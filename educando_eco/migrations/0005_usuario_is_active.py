# Generated by Django 4.2.1 on 2023-05-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educando_eco', '0004_usuario_groups_usuario_is_staff_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]