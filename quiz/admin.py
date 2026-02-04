from django.contrib import admin
from .models import BlockAttempt


@admin.register(BlockAttempt)
class BlockAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'block_number', 'score', 'total', 'percentage', 'taken_at')
    list_filter = ('subject', 'block_number', 'taken_at')
    search_fields = ('user__username', 'subject')
    readonly_fields = ('taken_at',)

