from apscheduler.schedulers.blocking import BlockingScheduler
from flask.ext.script import Command


from app.common.resources import logger
from app.workers.notification_job import NotificationJob
from app.workers.transfer_payments_jobs import TransferJob


class CronJobTaskRunner(Command):
    def run(self):
        scheduler = BlockingScheduler()
        cron_jobs = [NotificationJob(), TransferJob()]

        for cron_job in cron_jobs:
            trigger = cron_job.trigger()
            scheduler.add_job(cron_job.run, **trigger )
        logger.info('running CronJobTaskRunner')
        scheduler.start()
