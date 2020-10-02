# Generated by Django 2.1.5 on 2020-03-27 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('ContactUs_id', models.AutoField(primary_key=True, serialize=False)),
                ('ContactUs_top', models.TextField(max_length=50)),
                ('ContactUs_Number', models.TextField(max_length=50)),
                ('ContactUs_EmailID', models.CharField(blank=True, max_length=255, null=True)),
                ('ContactUs_Status', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
            ],
            options={
                'db_table': 'ContactUs',
            },
        ),
    ]
