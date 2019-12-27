import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from users.models import User


def delete_temp_users():
    for user in User.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(hours=1),
                                    email__endswith=''):
        pass


class AnalyticsScheduler:
    scheduler = BackgroundScheduler()

    @staticmethod
    def start_deleting():
        pass
        # AnalyticsScheduler.scheduler.add_job(sync_with_kpi_rozklad, trigger='cron', minute='1')
        # print(RozkladScheduler.scheduler.get_jobs())
        # RozkladScheduler.scheduler.start()
