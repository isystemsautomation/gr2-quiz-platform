from django.db import models
from django.contrib.auth.models import User


class BlockAttempt(models.Model):
    """Stores quiz attempt results for each block."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)  # electrotehnica, legislatie-gr-2, norme-tehnice-gr-2
    block_number = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()  # total questions in block
    percentage = models.FloatField()
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-taken_at']
        indexes = [
            models.Index(fields=['user', 'subject', 'block_number']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.subject} Block {self.block_number}: {self.score}/{self.total}"

