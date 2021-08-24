from django.db import models


from common.models import GenericPerson


class Teacher(GenericPerson):
    disciplines = models.CharField(max_length=50, default='None')
