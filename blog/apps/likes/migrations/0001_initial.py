# Generated by Django 2.1.5 on 2019-07-25 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(verbose_name='被点赞对象id')),
                ('likes_num', models.IntegerField(default=0, verbose_name='点赞数量')),
            ],
            options={
                'verbose_name': '点赞总数',
                'verbose_name_plural': '点赞总数',
            },
        ),
        migrations.CreateModel(
            name='LikeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='被点赞对象id')),
                ('liked_time', models.DateField(auto_now_add=True, verbose_name='点赞时间')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '用户点赞记录',
                'verbose_name_plural': '用户点赞记录',
            },
        ),
    ]
