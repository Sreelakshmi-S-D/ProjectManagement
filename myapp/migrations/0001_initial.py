# Generated by Django 5.0.1 on 2024-01-02 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_date', models.DateField()),
                ('Emp_code', models.IntegerField()),
                ('emp_name', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
            ],
        ),
    ]