# Generated migration for Question model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('electrotehnica', 'Electrotehnică'), ('legislatie-gr-2', 'Legislație GR. 2'), ('norme-tehnice-gr-2', 'Norme Tehnice GR. 2')], max_length=50)),
                ('qid', models.PositiveIntegerField()),
                ('block_number', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('option_a', models.TextField()),
                ('option_b', models.TextField()),
                ('option_c', models.TextField()),
                ('correct', models.CharField(blank=True, choices=[('a', 'A'), ('b', 'B'), ('c', 'C')], max_length=1, null=True)),
                ('explanation', models.TextField(blank=True, default='')),
                ('image_base', models.CharField(blank=True, default='', max_length=255)),
                ('edited_at', models.DateTimeField(blank=True, null=True)),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_questions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['subject', 'qid'],
            },
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['subject', 'block_number'], name='quiz_questi_subject_123456_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('subject', 'qid')},
        ),
    ]

