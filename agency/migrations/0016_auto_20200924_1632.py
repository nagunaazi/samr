# Generated by Django 2.2.8 on 2020-09-24 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0015_auto_20200924_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyrequestkybp',
            name='ag_title',
            field=models.CharField(choices=[('Ms', 'Ms'), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('M/s', 'M/s')], default='Mr', max_length=20),
        ),
    ]
