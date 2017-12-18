# Generated by Django 2.0 on 2017-12-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('surname', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240)),
            ],
        ),
        migrations.AddField(
            model_name='developer',
            name='educations',
            field=models.ManyToManyField(blank=True, related_name='developers', to='developers.Education'),
        ),
        migrations.AddField(
            model_name='developer',
            name='employment_history',
            field=models.ManyToManyField(blank=True, related_name='developers_history', to='developers.Company'),
        ),
        migrations.AddField(
            model_name='developer',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='developers', to='developers.Skill'),
        ),
    ]
