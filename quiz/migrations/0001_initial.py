# Generated migration for BlockAttempt model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('block_number', models.PositiveIntegerField()),
                ('score', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('percentage', models.FloatField()),
                ('taken_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-taken_at'],
            },
        ),
        migrations.AddIndex(
            model_name='blockattempt',
            index=models.Index(fields=['user', 'subject', 'block_number'], name='quiz_blocka_user_id_123456_idx'),
        ),
    ]

