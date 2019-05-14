from django.db import models
from django.conf import settings
from handleit.apps.core.models import TimeStampedModel
import uuid as uuid_lib
# Create your models here.


class TaskList(TimeStampedModel):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()


class ListAccess(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)


class Task(TimeStampedModel):
    URGENCY_LOW = 1
    URGENCY_NORMAL = 2
    URGENCY_HIGH = 3
    URGENCY_CRITICAL = 4

    URGENCY_LEVELS = (
        (URGENCY_LOW, 'Low'),
        (URGENCY_NORMAL, 'Moderate'),
        (URGENCY_HIGH, 'High'),
        (URGENCY_CRITICAL, 'Critical')
    )

    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    urgency = models.CharField(max_length=2, choices=URGENCY_LEVELS)
    task_completed = models.BooleanField(default=False)

