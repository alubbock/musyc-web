# Generated by Django 3.0.3 on 2020-03-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musycweb', '0003_e0_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='deleted_date',
            field=models.DateTimeField(default=None, editable=False, null=True),
        ),
    ]
