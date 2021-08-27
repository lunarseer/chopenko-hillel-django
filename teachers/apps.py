from django.apps import AppConfig


class TeachersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teachers'

    def ready(self) -> None:
        from common.handlers import firstname_lastname_edit_handler