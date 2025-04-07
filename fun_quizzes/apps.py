from django.apps import AppConfig

class TestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
    verbose_name = '테스트 앱'
