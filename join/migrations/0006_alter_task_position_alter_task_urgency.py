# Generated by Django 5.1 on 2024-09-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0005_alter_team_members_alter_team_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='position',
            field=models.CharField(choices=[('todo', 'Todo'), ('in_progress', 'In progress'), ('await_feedback', 'Await feedback'), ('done', 'Done')], max_length=15),
        ),
        migrations.AlterField(
            model_name='task',
            name='urgency',
            field=models.CharField(blank=True, choices=[(None, 'No Priority'), ('low', 'Low'), ('medium', 'Medium'), ('urgent', 'Urgent')], max_length=10, null=True),
        ),
    ]
