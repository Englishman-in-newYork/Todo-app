# Generated by Django 3.1.4 on 2021-06-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='status_task',
            field=models.CharField(choices=[('Waiting', 'Waiting'), ('Implementation', 'Implementation'), ('Verifying', 'Verifying'), ('Releasing', 'Releasing')], default='Waiting', max_length=50, verbose_name='Status of task'),
        ),
    ]