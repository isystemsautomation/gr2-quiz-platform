from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Empty migration left in place to avoid conflicts with an existing
    0003 migration in this project. The actual BlockNote model is
    created in 0004_blocknote.py.
    """

    dependencies = [
        ("quiz", "0002_question"),
    ]

    operations = []

