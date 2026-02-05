from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # Chain after 0003_blocknote (which is now an empty migration),
        # so there is a single leaf in the migration graph.
        ("quiz", "0003_blocknote"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlockNote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        max_length=50,
                        choices=[
                            ("electrotehnica", "Electrotehnică"),
                            ("legislatie-gr-2", "Legislație GR. 2"),
                            ("norme-tehnice-gr-2", "Norme Tehnice GR. 2"),
                        ],
                    ),
                ),
                ("block_number", models.PositiveIntegerField()),
                ("note", models.TextField(blank=True, default="")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["user", "subject", "block_number"],
                "unique_together": {("user", "subject", "block_number")},
            },
        ),
    ]


