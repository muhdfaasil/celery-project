from celery import shared_task
import time


@shared_task
def add_numbers(x, y):
    """A simple task that adds two numbers after a delay."""
    time.sleep(5)  # Simulate some work
    result = x + y
    print(f"Task completed: {x} + {y} = {result}")
    return result


@shared_task
def send_email_task(email, subject, message):
    """A simulated email sending task."""
    time.sleep(3)  # Simulate email sending
    print(f"Email sent to {email} with subject: {subject}")
    return f"Email sent to {email}"


@shared_task
def process_data_task(data):
    """A task that processes some data."""
    time.sleep(2)  # Simulate data processing
    processed = f"Processed: {data}"
    print(processed)
    return processed

