# Generated by Django 4.2.20 on 2025-03-23 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialite', '0003_alter_specialite_designation'),
        ('Employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': 'Cet email est déjà utilisé.'}, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, help_text="Prénom de l'agent", max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='grade',
            field=models.CharField(blank=True, help_text='Grade', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='num_tel',
            field=models.CharField(blank=True, error_messages={'unique': 'Ce numéro est déjà utilisé.'}, max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='specialty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specialite.specialite'),
        ),
    ]
