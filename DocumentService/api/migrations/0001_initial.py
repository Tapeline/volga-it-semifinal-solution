# Generated by Django 5.0.2 on 2024-10-26 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('pacient_id', models.IntegerField()),
                ('hospital_id', models.IntegerField()),
                ('doctor_id', models.IntegerField()),
                ('room', models.CharField()),
                ('data', models.TextField()),
            ],
        ),
    ]
