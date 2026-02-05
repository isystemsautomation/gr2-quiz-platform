from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    # This file is kept only to avoid import errors if it was already
    # referenced somewhere; the real BlockNote creation now lives in
    # 0004_blocknote. This migration does nothing.

    dependencies = [
        ("quiz", "0002_question"),
    ]

    operations = []

