from django.db import models

from common.models import GenericPerson


class Teacher(GenericPerson):
    dicsiplines = models.JSONField(default=list)