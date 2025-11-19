from django.db import models
from django.utils import timezone


class TaskResult(models.Model):
    """Model to store Celery task results in the database."""
    
    TASK_TYPES = [
        ('add_numbers', 'Add Numbers'),
        ('send_email', 'Send Email'),
        ('process_data', 'Process Data'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('started', 'Started'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True, db_index=True)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_data = models.JSONField(default=dict, help_text="Input parameters for the task")
    result = models.TextField(blank=True, null=True, help_text="Task result/output")
    error = models.TextField(blank=True, null=True, help_text="Error message if task failed")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True, help_text="Task duration in seconds")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task Result'
        verbose_name_plural = 'Task Results'
    
    def __str__(self):
        return f"{self.task_type} - {self.task_id} - {self.status}"

