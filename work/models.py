from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse


class Task(models.Model):

    def validate_date(date):
        if date < timezone.now().date():
            raise ValidationError("deadline cannot be in the past")

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'office_tag': 2}, related_name='task_sender')
    title = models.CharField(max_length=100)
    description = models.TextField()
    sender_file = models.FileField(upload_to='work/employer/', blank=True)
    reciever_file = models.FileField(upload_to='work/employee/', blank=True)
    date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(default=datetime.date.today, validators=[validate_date])
    status = models.BooleanField(default=False)
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'office_tag': 1}, related_name='task_reciever')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('work-employertaskview', kwargs={'username': self.sender})
