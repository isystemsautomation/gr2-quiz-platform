from django.contrib import admin
from .models import Question, BlockAttempt


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'qid', 'block_number', 'correct', 'short_explanation', 'edited_by', 'edited_at')
    list_filter = ('subject', 'block_number', 'correct')
    search_fields = ('qid', 'text', 'option_a', 'option_b', 'option_c')
    fields = ('subject', 'qid', 'block_number', 'text', 'option_a', 'option_b', 'option_c', 
              'correct', 'explanation', 'image_base', 'edited_by', 'edited_at')
    readonly_fields = ('edited_by', 'edited_at')
    
    def short_explanation(self, obj):
        if obj.explanation:
            return obj.explanation[:50] + '...' if len(obj.explanation) > 50 else obj.explanation
        return '-'
    short_explanation.short_description = 'Explanation'


@admin.register(BlockAttempt)
class BlockAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'block_number', 'score', 'total', 'percentage', 'taken_at')
    list_filter = ('subject', 'block_number', 'taken_at')
    search_fields = ('user__username', 'subject')
    readonly_fields = ('taken_at',)

