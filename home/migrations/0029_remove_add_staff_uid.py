# Generated by Django 4.2.1 on 2023-10-04 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_add_staff_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='add_staff',
            name='uid',
        ),
    ]
