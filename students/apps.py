from django.apps import AppConfig


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'

    def ready(self) -> None:
        from common.handlers import firstname_lastname_edit_handler     # noqa: F401
