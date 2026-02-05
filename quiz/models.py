from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """Stores quiz questions in the database."""
    SUBJECT_CHOICES = [
        ('electrotehnica', 'Electrotehnică'),
        ('legislatie-gr-2', 'Legislație GR. 2'),
        ('norme-tehnice-gr-2', 'Norme Tehnice GR. 2'),
    ]
    
    CORRECT_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ]
    
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    qid = models.PositiveIntegerField()  # question id from JSON
    block_number = models.PositiveIntegerField()
    text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    correct = models.CharField(max_length=1, choices=CORRECT_CHOICES, null=True, blank=True)
    explanation = models.TextField(blank=True, default="")
    image_base = models.CharField(max_length=255, blank=True, default="")
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_questions')
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['subject', 'qid']
        unique_together = [['subject', 'qid']]
        indexes = [
            models.Index(fields=['subject', 'block_number']),
        ]

    def __str__(self):
        return f"{self.subject} Q{self.qid} (Block {self.block_number})"


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


class BlockNote(models.Model):
    """
    Personal note per user / subject / block.
    Visible only to the owner. Used for \"my comments\" on a block.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, choices=Question.SUBJECT_CHOICES)
    block_number = models.PositiveIntegerField()
    note = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'subject', 'block_number']]
        ordering = ['user', 'subject', 'block_number']

    def __str__(self):
        return f"Note {self.user.username} {self.subject} B{self.block_number}"

