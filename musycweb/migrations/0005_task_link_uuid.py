# Generated by Django 3.0.3 on 2020-03-21 18:58

from django.db import migrations, models
import django.db.models.deletion
from django.db.models import F


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    DatasetTask = apps.get_model("musycweb", "DatasetTask")
    db_alias = schema_editor.connection.alias

    DatasetTask.objects.using(db_alias).update(task_id=F('task_uuid'))


def reverse_func(apps, schema_editor):
    DatasetTask = apps.get_model("musycweb", "DatasetTask")
    TaskResult = apps.get_model("django_celery_results", "TaskResult")
    db_alias = schema_editor.connection.alias

    for dt in DatasetTask.objects.using(db_alias).all():
        dt.task = TaskResult.objects.using(db_alias).get(task_id=dt.task_uuid)
        dt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_results', '0007_remove_taskresult_hidden'),
        ('musycweb', '0004_deleted_flag'),
    ]

    operations = [
        migrations.RunPython(lambda a, b: None, reverse_func),
        migrations.RemoveField(
            model_name='datasettask',
            name='task',
        ),
        migrations.AddField(
            model_name='datasettask',
            name='task',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    db_constraint=False,
                                    to='django_celery_results.TaskResult',
                                    to_field='task_id'),
        ),
        migrations.RunPython(forwards_func),
        migrations.AlterField(
            model_name='datasettask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    db_constraint=False,
                                    to='django_celery_results.TaskResult',
                                    to_field='task_id'),
        ),
        migrations.RemoveField(
            model_name='datasettask',
            name='task_uuid',
        )
    ]
