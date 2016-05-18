# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0008_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='id',
        ),
        migrations.RemoveField(
            model_name='listmanager',
            name='id',
        ),
        migrations.AddField(
            model_name='listmanager',
            name='manager_text',
            field=models.CharField(default='UNNAMED MANAGER', max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_text',
            field=models.CharField(default='UNNAMED ITEM', max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='itemlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vote.ItemList'),
        ),
        migrations.AlterField(
            model_name='listmanager',
            name='itemlist',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vote.ItemList'),
        ),
    ]
