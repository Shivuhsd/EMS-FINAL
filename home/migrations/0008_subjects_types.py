# Generated by Django 4.2.5 on 2023-09-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_dept_subject_student_link_elective_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='types',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
