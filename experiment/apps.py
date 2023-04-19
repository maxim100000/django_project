from django.apps import AppConfig


class ExperimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'experiment'

    def ready(self):
        from .scheduler import week_schedular
        from .tasks import send

        week_schedular.add_job(
            send,
            'cron',
            day_of_week='fri'
        )

        # week_schedular.start()
