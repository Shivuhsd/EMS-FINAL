# Generated by Django 4.2.1 on 2023-10-01 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_remove_link_student_alter_add_staff_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_seat',
            name='cour',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]