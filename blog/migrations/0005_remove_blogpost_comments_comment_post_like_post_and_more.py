# Generated by Django 4.2.5 on 2023-10-05 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_comments_alter_blogpost_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost'),
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.blogpost'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
