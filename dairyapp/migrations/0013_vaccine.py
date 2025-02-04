# Generated by Django 3.0.5 on 2023-12-18 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dairyapp', '0012_auto_20231212_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccination_type', models.CharField(max_length=64)),
                ('nearby_hospital', models.CharField(max_length=100)),
                ('prefered_date', models.DateField()),
                ('check_status', models.CharField(max_length=50)),
                ('eartag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairyapp.farmer_eartag_application')),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dairyapp.farmer_registration')),
            ],
        ),
    ]
