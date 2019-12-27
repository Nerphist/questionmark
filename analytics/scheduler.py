import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from analytics.models import SolvedTest
from api_tests.models import AnonymousLink
from users.models import User


def delete_temp_users():
    for user in User.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(hours=1),
                                    email__endswith='@anonmail.com'):
        if user.is_student():
            for test in SolvedTest.objects.filter(student=user.student).all():
                if not test.is_checked:
                    test.check_test()
            user.student.delete()
            user.delete()
    for link in AnonymousLink.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(hours=24)):
        link.delete()


class AnalyticsScheduler:
    scheduler = BackgroundScheduler()

    @staticmethod
    def start_deleting():
        AnalyticsScheduler.scheduler.add_job(delete_temp_users, trigger='cron', minute='1')
        AnalyticsScheduler.scheduler.start()
