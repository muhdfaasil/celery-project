from django.shortcuts import render
from django.http import JsonResponse
from .tasks import add_numbers, send_email_task, process_data_task


def index(request):
    """Main page with task triggers."""
    return render(request, 'tasks/index.html')


def trigger_add_task(request):
    """Trigger the add_numbers task."""
    if request.method == 'POST':
        try:
            x = int(request.POST.get('x', 5))
            y = int(request.POST.get('y', 10))
            task = add_numbers.delay(x, y)
            return JsonResponse({
                'status': 'success',
                'task_id': task.id,
                'message': f'Task started: Adding {x} + {y}'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)


def trigger_email_task(request):
    """Trigger the send_email_task."""
    if request.method == 'POST':
        try:
            email = request.POST.get('email', 'test@example.com')
            subject = request.POST.get('subject', 'Test Email')
            message = request.POST.get('message', 'This is a test message')
            task = send_email_task.delay(email, subject, message)
            return JsonResponse({
                'status': 'success',
                'task_id': task.id,
                'message': f'Email task started for {email}'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)


def trigger_process_task(request):
    """Trigger the process_data_task."""
    if request.method == 'POST':
        try:
            data = request.POST.get('data', 'Sample data')
            task = process_data_task.delay(data)
            return JsonResponse({
                'status': 'success',
                'task_id': task.id,
                'message': f'Processing task started for: {data}'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)

