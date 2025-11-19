from django.contrib import admin
from .models import TaskResult


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_type', 'status', 'created_at', 'completed_at', 'duration_seconds')
    list_filter = ('task_type', 'status', 'created_at')
    search_fields = ('task_id', 'task_type', 'result', 'error')
    readonly_fields = ('task_id', 'created_at', 'completed_at', 'duration_seconds')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('task_id', 'task_type', 'status')
        }),
        ('Input/Output', {
            'fields': ('input_data', 'result', 'error')
        }),
        ('Timing', {
            'fields': ('created_at', 'completed_at', 'duration_seconds')
        }),
    )

