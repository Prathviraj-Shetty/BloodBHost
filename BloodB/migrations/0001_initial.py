# Generated by Django 4.1.3 on 2022-12-09 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DONATION',
            fields=[
                ('did', models.AutoField(primary_key=True, serialize=False)),
                ('ddate', models.DateField()),
                ('dqty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PERSON',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.CharField(max_length=15)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=122)),
                ('bgroup', models.CharField(max_length=10)),
                ('MIssues', models.CharField(max_length=122)),
            ],
        ),
        migrations.CreateModel(
            name='RECEIVE',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('rdate', models.DateTimeField()),
                ('rqty', models.IntegerField()),
                ('hospital_name', models.CharField(max_length=122)),
                ('rbgroup', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='STOCK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sbgroup', models.CharField(max_length=10)),
                ('qty', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='receives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloodB.person')),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloodB.receive')),
            ],
        ),
        migrations.CreateModel(
            name='donates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloodB.donation')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BloodB.person')),
            ],
        ),
    ]
