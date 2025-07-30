from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from django.core.mail import send_mail



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        # Send email
        send_mail(
            subject='New Task Created',
            message=f'Your task "{task.title}" is created and due on {task.due_date}.',
            from_email='you@example.com',
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        task = serializer.save()

        # Optional: send update email
        send_mail(
            subject='Task Updated',
            message=f'Your task "{task.title}" was updated. New status: {task.status}.',
            from_email='you@example.com',
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )



