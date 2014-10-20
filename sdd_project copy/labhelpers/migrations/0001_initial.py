# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correct_answer_text', models.CharField(max_length=200)),
                ('wrong_answer_text_1', models.CharField(default=b'', max_length=200)),
                ('wrong_answer_text_2', models.CharField(default=b'', max_length=200)),
                ('wrong_answer_text_3', models.CharField(default=b'', max_length=200)),
                ('wrong_answer_text_4', models.CharField(default=b'', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab_id', models.IntegerField()),
                ('lab_name', models.CharField(max_length=200)),
                ('lab_type', models.CharField(default=b'STATIC', max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_id', models.IntegerField()),
                ('question_text', models.TextField()),
                ('question_hint', models.TextField()),
                ('lab', models.ForeignKey(to='labhelpers.Lab')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_id', models.IntegerField()),
                ('topic_name', models.CharField(max_length=200)),
                ('coach_data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=50)),
                ('user_rin', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(to='labhelpers.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='labhelpers.Question'),
            preserve_default=True,
        ),
    ]
