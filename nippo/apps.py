from django.apps import AppConfig


class NippoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nippo'
    verbose_name = "日報アプリ"#apps.pyのクラス内で、変数「verbose_name」を指定すると、アプリ名が変更になります5-6