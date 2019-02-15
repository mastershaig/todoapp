from django.db import models
from django.utils import timezone
from django.conf import settings


class Todolist(models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=False)
    status = models.BooleanField(default=True, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name

class Share(models.Model):
    todoer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    todoes = models.ForeignKey(Todolist, on_delete=models.CASCADE)
    type = models.IntegerField(default=0, choices=(
        (0, "View only"),
        (1, "Can Comment")
    ))

class Messenger(models.Model):
    todoapp = models.ForeignKey('Todolist', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    preview = models.BooleanField(default=False)
    # logs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return "Todoapp-{}-{}".format(self.todoapp.name, self.user.email)

