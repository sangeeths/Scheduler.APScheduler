from apscheduler.scheduler import SchedulerAlreadyRunningError
from apscheduler.scheduler import Scheduler as APScheduler
from datetime import datetime, date, time, timedelta
import time
import logging

class SchedulerNotRunningError(Exception):
    """
    Raised when attempting to stop the scheduler 
    when it is not running.
    """
    def __str__(self):
        return 'Attempting to stop a Scheduler which is not running'


logging.basicConfig(filename='/tmp/log', level=logging.DEBUG,
        format='[%(asctime)s]: %(levelname)s : %(message)s')


# Job Store details
# todo: read these info from file
__db_username = 'root'
__db_password = 'root123'
__db_location = 'localhost'
__db_dbname   = 'jobstore'

# Job Store URL to be passed to scheduler configure
# url = 'mysql://root:root123@localhost/jobstore'
__db_url = 'mysql://%s:%s@%s/%s' % \
           (__db_username, __db_password, \
            __db_location, __db_dbname)

# use 'default' as the name of your job store
# jbs = Job Store
__jbs_name = 'default'

# todo: change the table name 
# jbs_tn = Job Store Table Name 
__jbs_tn    = 'Framework_Jobs'
__jbs_class = 'apscheduler.jobstore.%s.class' % __jbs_name
__jbs_url   = 'apscheduler.jobstore.%s.url' % __jbs_name
__jbs_table = 'apscheduler.jobstore.%s.tablename' % __jbs_name
__jbs_sqlalchemy = 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore'
# APScheduler (preferred) default configuration
# todo: read these info from a .ini file
#       from a configurable location
#
_g_aps_default_config = {
    'apscheduler.misfire_grace_time' : 1,
    'apscheduler.coalesce'           : True,
    'apscheduler.daemonic'           : True,
    'apscheduler.standalone'         : True,
    __jbs_class : __jbs_sqlalchemy,
    __jbs_url   : __db_url,
    __jbs_table : __jbs_tn
}

class Scheduler:
    """
    Wrapper for APScheduler.
    """

    # Handle to APScheduler
    __aps = APScheduler(_g_aps_default_config)

    def __init__(self, aps_config={}):
        self.configure(aps_config) 

    def configure(self, aps_config={}):
        """
        Re-configure the Scheduler with the 
        user preferred options
        """
        if Scheduler.__aps.running: 
            raise SchedulerAlreadyRunningError
        if aps_config: Scheduler.__aps.configure(aps_config)

    def start(self):
        """
        Start the Scheduler. 
        Raise SchedulerAlreadyRunningError 
        if already running.
        """
        if Scheduler.__aps.running: 
            raise SchedulerAlreadyRunningError
        Scheduler.__aps.start()

    def stop(self):
        """
        Stop the Scheduler.
        Raise SchedulerNotRunningError
        if not running.
        """
        if not Scheduler.__aps.running: 
            raise SchedulerNotRunningError
        Scheduler.__aps.shutdown()

    def is_running(self):
        """
        Scheduler is running or not.
        """
        return Scheduler.__aps.running

    def at(self, func, date, args=None, **options):
        return Scheduler.__aps.add_date_job(func, date, args, options)

    def schedule_at(self, date, args=None, **options):
        def decorator(func):
            func.job = Scheduler.__aps.add_date_job(func, date, args, options)
            return func
        return decorator

    def every(self, func, weeks=0, days=0, hours=0, minutes=0, 
              seconds=0, start_date=None, args=None, kwargs=None, 
              **options): 
        return Scheduler.__aps.add_interval_job(func, weeks, days, 
                                                hours, minutes, seconds, 
                                                start_date, args, options)

    def schedule_every(self, weeks=0, days=0, hours=0, 
                       minutes=0, seconds=0, start_date=None, 
                       args=None, kwargs=None, **options): 
        def decorator(func):
            func.job = Scheduler.__aps.add_interval_job(func, weeks, days, 
                                                hours, minutes, seconds, 
                                                start_date, args, options)
            return func
        return decorator

    def after(self, func, weeks=0, days=0, hours=0, minutes=0, 
              seconds=0, args=None, kwargs=None, **options): 
        alarm_time = datetime.now() + \
                     timedelta(weeks=weeks, days=days, 
                               hours=hours, minutes=minutes, 
                               seconds=seconds)
        return Scheduler.__aps.add_date_job(func, alarm_time, args, options)

    def schedule_after(self, weeks=0, days=0, hours=0, minutes=0, 
                       seconds=0, args=None, kwargs=None, **options): 
        def decorator(func):
            alarm_time = datetime.now() + timedelta(weeks=weeks, days=days, 
                         hours=hours, minutes=minutes, seconds=seconds)
            func.job = Scheduler.__aps.add_date_job(func, alarm_time, args, options)
            return func
        return decorator

    def cron(self, func, year='*', month='*', day='*', 
             week='*', day_of_week='*', hour='*', 
             minute='*', second='*', start_date=None, 
             args=None, kwargs=None, **options):
        return Scheduler.__aps.add_cron_job(func, year, month, day, week, 
                                            day_of_week, hour, minute, second, 
                                            start_date, args, options)

    def schedule_cron(self, year='*', month='*', day='*', 
                      week='*', day_of_week='*', hour='*', 
                      minute='*', second='*', start_date=None, 
                      args=None, kwargs=None, **options):
        def decorator(func):
            func.job = Scheduler.__aps.add_cron_job(func, year, month, day, week, 
                                            day_of_week, hour, minute, second, 
                                            start_date, args, options)
            return func
        return decorator


