from django.db import models


from common.models import GenericPerson


class Teacher(GenericPerson):
    disciplines = models.JSONField(default=list)
