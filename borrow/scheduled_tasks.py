from apscheduler.schedulers.background import BackgroundScheduler

from notifications.notification import send_overdue_message


def schedule_message():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_overdue_message, "interval", hours=24, id="message_001", replace_existing=True)
    scheduler.start()
