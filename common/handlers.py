from django.db.models.signals import pre_save
from django.dispatch import receiver

from students.models import Student
from teachers.models import Teacher


@receiver(pre_save, sender=Student)
@receiver(pre_save, sender=Teacher)
def firstname_lastname_edit_handler(sender, **kwargs):
    if firstname := kwargs['instance'].firstname:
        kwargs['instance'].firstname = firstname.capitalize()
    if lastname := kwargs['instance'].lastname:
        kwargs['instance'].lastname = lastname.capitalize()
