# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 09:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import members.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=members.models.rename_photo, verbose_name='Photo')),
                ('first_name', models.CharField(max_length=100, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adresse')),
                ('prefix', models.IntegerField(choices=[(10, '+352'), (11, '+32'), (13, '+49'), (12, '+33')], default=10, verbose_name='Préfix')),
                ('phone', models.IntegerField(blank=True, null=True, verbose_name='Tél. fixe')),
                ('mobile', models.IntegerField(blank=True, null=True, verbose_name='Tél. mobile')),
                ('email', models.EmailField(max_length=254)),
                ('start_date', models.DateField(verbose_name='Date de début')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Date de fin')),
                ('status', models.IntegerField(choices=[(0, 'actif'), (1, 'honoraire'), (2, 'aspirant (wouldbe)'), (3, 'inactif (standby)')], default=0, verbose_name='Statut')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=25, verbose_name='Saison')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Titre')),
                ('type', models.IntegerField(choices=[(0, 'comité'), (1, 'commission'), (2, 'other')], default=0, verbose_name='Type')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.RoleType'),
        ),
        migrations.AlterUniqueTogether(
            name='role',
            unique_together=set([('member', 'type')]),
        ),
    ]