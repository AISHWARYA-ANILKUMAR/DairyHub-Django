# Generated by Django 3.0.5 on 2023-11-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0004_auto_20231110_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmer_eartag_re_application',
            name='missing_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='farmer_eartag_re_application',
            name='new_eartag_regi_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='farmer_eartag_re_application',
            name='prev_eartag_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='farmer_eartag_re_application',
            name='prev_eartag_regi_date',
            field=models.DateField(),
        ),
    ]
