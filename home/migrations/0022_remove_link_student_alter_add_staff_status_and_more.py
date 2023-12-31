# Generated by Django 4.2.1 on 2023-10-01 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_add_staff_status_alter_room_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='student',
        ),
        migrations.AlterField(
            model_name='add_staff',
            name='status',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.add_staff'),
        ),
        migrations.CreateModel(
            name='Student_seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(blank=True, max_length=4)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studentdata')),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='st',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='home.student_seat'),
            preserve_default=False,
        ),
    ]
