from flask.ext.script import Server, Manager

from app.workers.notification_job import NotificationJob
from app.workers.transfer_payments_jobs import TransferJob
from app.workers.twitter_worker import TwitterWorker
from runserver import app

manager = Manager(app)

manager.add_command('runserver', Server())
manager.add_command('twitter_stream_task', TwitterWorker())
manager.add_command('notification_job', NotificationJob())
manager.add_command('transfer_job', TransferJob())

if __name__ == '__main__':
    manager.run()
