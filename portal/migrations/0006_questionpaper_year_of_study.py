# Generated by Django 5.0.1 on 2024-12-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_questionpaper_delete_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpaper',
            name='year_of_study',
            field=models.CharField(choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')], default='1st Year', max_length=20),
            preserve_default=False,
        ),
    ]
