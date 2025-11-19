from celery import shared_task
import time
from django.utils import timezone
from .models import TaskResult


@shared_task(bind=True)
def add_numbers(self, x, y):
    """A simple task that adds two numbers after a delay."""
    task_id = self.request.id
    start_time = timezone.now()
    
    # Create task result record
    task_result = TaskResult.objects.create(
        task_id=task_id,
        task_type='add_numbers',
        status='started',
        input_data={'x': x, 'y': y}
    )
    
    try:
        time.sleep(5)  # Simulate some work
        result = x + y
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with success
        task_result.status = 'success'
        task_result.result = str(result)
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        print(f"Task completed: {x} + {y} = {result}")
        return result
    except Exception as e:
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with error
        task_result.status = 'failure'
        task_result.error = str(e)
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        raise


@shared_task(bind=True)
def send_email_task(self, email, subject, message):
    """A simulated email sending task."""
    task_id = self.request.id
    start_time = timezone.now()
    
    # Create task result record
    task_result = TaskResult.objects.create(
        task_id=task_id,
        task_type='send_email',
        status='started',
        input_data={'email': email, 'subject': subject, 'message': message}
    )
    
    try:
        time.sleep(3)  # Simulate email sending
        result = f"Email sent to {email}"
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with success
        task_result.status = 'success'
        task_result.result = result
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        print(f"Email sent to {email} with subject: {subject}")
        return result
    except Exception as e:
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with error
        task_result.status = 'failure'
        task_result.error = str(e)
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        raise


@shared_task(bind=True)
def process_data_task(self, data):
    """A task that processes some data."""
    task_id = self.request.id
    start_time = timezone.now()
    
    # Create task result record
    task_result = TaskResult.objects.create(
        task_id=task_id,
        task_type='process_data',
        status='started',
        input_data={'data': data}
    )
    
    try:
        time.sleep(2)  # Simulate data processing
        processed = f"Processed: {data}"
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with success
        task_result.status = 'success'
        task_result.result = processed
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        print(processed)
        return processed
    except Exception as e:
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Update task result with error
        task_result.status = 'failure'
        task_result.error = str(e)
        task_result.completed_at = end_time
        task_result.duration_seconds = duration
        task_result.save()
        
        raise

