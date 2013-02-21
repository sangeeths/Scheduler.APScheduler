"""
Scheduler

A wrapper for APScheduler which provides
the following functions (and its decorators):

 [1] at()    : execute func at given date & time 
 [2] every() : execute func every w, d, h, s, m 
 [3] after() : execute func after given date & time 
 [4] cron()  : execute func based on various expressions 
               on each field - y, m, d, w, dow, h, m, s 
"""

from apscheduler.scheduler import SchedulerAlreadyRunningError
from apscheduler.scheduler import Scheduler as APScheduler
from datetime import datetime, timedelta
import logging

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Logging 
#
# __g_log_file      : log file name for the scheduler
#                     [default: /tmp/scheduler_logs]
# __g_log_level     : log level for the scheduler
#                     [default: logging.DEBUG]  
# __g_log_format    : logging format for the scheduler
#                     [default: "date & time : level : msg"]
#
# TODO: Sechudler.configure() should accept the above
#       mentioned logging parameters from the user and 
#       configure the logging.basicConfig accordingly
#       (or) read these input from a config file.
#
__g_log_file   = '/tmp/scheduler_logs'
__g_log_level  = logging.DEBUG
__g_log_format = '[%(asctime)s]: %(levelname)s : %(message)s'

# configure logging
logging.basicConfig(filename=__g_log_file, 
                    level=__g_log_level, 
                    format=__g_log_format)
#
# End of Logging
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Exception Classes
#
class SchedulerNotRunningError(Exception):
    """
    Raised when attempting to stop the scheduler
    when it is not running.
    """
    def __str__(self):
        return 'Attempting to stop a Scheduler ' \
               'which is not running'

class UnSupportedParameter(Exception):
    """
    Raised when attempting to pass 
    an unsupported parameter.
    """
    def __str__(self):
        return 'Attempting to pass ' \
               'an unsupported parameter.'

class UnSupportedFeature(Exception):
    """
    Raised when attempting to invoke a 
    functionality which is not supported.
    """
    def __str__(self):
        return 'This feature is not ' \
               'currently supported.'
#
# Add more exception classes above!
#
# End of Exception Classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Database Configuration
#
# __db_username : username for db [default: root]
# __db_password : password for db [default: root123]
# __db_location : ip addr or name [default: localhost]
# __db_dbname   : name of the db  [default: jobstore]
#
# TODO: read these parameters from a config file
# TODO: update __db_dbname with an appropriate name
# TODO: get rid of the plain text password
#
__db_username = 'root'
__db_password = 'root123'
__db_location = 'localhost'
__db_dbname   = 'jobstore'

#
# configure the url which will be passed to the 
# Scheduler.configure to configure the jobstore.
# url format: 
#   'mysql://root:root123@localhost/jobstore'
#
__db_url = 'mysql://%s:%s@%s/%s' % \
           (__db_username, __db_password, \
            __db_location, __db_dbname)
#
# End of Exception Classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# JobStore and Scheduler Configuration
# 
# __jbs = JoBStore
#
# __jbs_name    : name of the jobstore 
#                 [default: "default", this would be
#                           the default job store]
# __jbs_tn      : jobstore table name 
#                 [default: "Framework_Jobs"]
# __jbs_class   : apscheduler class name for default jobstore
#                 [default: apscheduler.jobstore.default.class]
# __jbs_url     : apscheduler class name for default url
#                 [default: apscheduler.jobstore.default.url]
# __jbs_table   : apscheduler class name for default table name
#                 [default: apscheduler.jobstore.default.tablename]
# __jbs_sqlalchemy : apscheduler class name for SQLAlchemy jobstore
# [default: apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore]
# 
# TODO: update __jbs_tn with appropriate table name
# TODO: read these parameters from a config file
#
__jbs_name  = 'default'
__jbs_tn    = 'Framework_Jobs'
__jbs_class = 'apscheduler.jobstore.%s.class' % __jbs_name
__jbs_url   = 'apscheduler.jobstore.%s.url' % __jbs_name
__jbs_table = 'apscheduler.jobstore.%s.tablename' % __jbs_name
__jbs_sqlalchemy = 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore'

# APScheduler (preferred) default configuration
# NOTE: do NOT use this config for now. 
#       for more info, refer readme file.
# NOTE: currently, persistant job storage is not supported
_g_aps_default_sql_config = {
    'apscheduler.misfire_grace_time' : 1,
    'apscheduler.coalesce'           : True,
    'apscheduler.daemonic'           : True,
    'apscheduler.standalone'         : True,
    __jbs_class : __jbs_sqlalchemy,
    __jbs_url   : __db_url,
    __jbs_table : __jbs_tn
}

# NOTE: use the following config for now (TEMPORARY)
#       it is RAMJobStore and not SQLAlchemyJobStore
_g_aps_default_ram_config = {
    'apscheduler.misfire_grace_time' : 1,
    'apscheduler.coalesce'           : True,
    'apscheduler.daemonic'           : True,
    'apscheduler.standalone'         : True,
}
#
# End of Exception Classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler Class
#
class Scheduler:
    """
    A wrapper for APScheduler.
     
    This provides functions (and decorators)
    at(), every(), after() and cron().
    """

    # Handle to APScheduler
    # NOTE: do not use SQL config for now; use RAM config.
    #       (TEMPORARY)
    # 
    #__aps = APScheduler(_g_aps_default_sql_config)
    __aps = APScheduler(_g_aps_default_ram_config)

    def __init__(self, aps_config={}):
        self.configure(aps_config) 

    def configure(self, aps_config={}):
        """
        Re-configure the Scheduler with the 
        user preferred parameters, if given.
        """
        if Scheduler.__aps.running: 
            raise SchedulerAlreadyRunningError
        if aps_config: 
            Scheduler.__aps.configure(aps_config)

    def start(self):
        """
        Start the Scheduler. 
        """
        if Scheduler.__aps.running: 
            raise SchedulerAlreadyRunningError
        Scheduler.__aps.start()

    def stop(self):
        """
        Stop the Scheduler.
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
        """
        Schedules a job to be completed
        _at_ a specific future date and time.

        func : name of the callable function 
        date : date and time to be called
        args : arguments to the function 'func'
        """
        return Scheduler.__aps.add_date_job(func, date, args, options)

    def schedule_at(self, date, args=None, **options):
        """
        Decorator for Scheduler.at()
        """
        def decorator(func):
            func.job = Scheduler.__aps.add_date_job(func, date, args, options)
            return func
        return decorator

    # TODO: Scheduler.every() uses APScheduler's add_interval_job()
    #       which currently does not support scheduling parameters 
    #       like year and month. Provide a patch to support this!
    def every(self, func, weeks=0, days=0, hours=0, minutes=0, 
              seconds=0, start_date=None, args=None, kwargs=None, 
              **options): 
        """
        Schedules a job to be completed for 
        _every_ specified weeks, days, hours, 
        minutes, and seconds starting from 
        the given start date and time.

        func    : name of the callable function
        weeks   : number of weeks to wait
        days    : number of days to wait
        hours   : number of hours to wait
        minutes : number of minutes to wait
        seconds : number of seconds to wait
        start_date: when to first execute the job 
                    and start the counter (default 
                    is after the given interval)
        args    : arguments to the function 'func'
        """
        return Scheduler.__aps.add_interval_job(func, weeks, days, 
                                                hours, minutes, seconds, 
                                                start_date, args, options)

    def schedule_every(self, weeks=0, days=0, hours=0, 
                       minutes=0, seconds=0, start_date=None, 
                       args=None, kwargs=None, **options): 
        """
        Decorator for Scheduler.every()
        """
        def decorator(func):
            func.job = Scheduler.__aps.add_interval_job(func, weeks, days, 
                                                hours, minutes, seconds, 
                                                start_date, args, options)
            return func
        return decorator

    def after(self, func, weeks=0, days=0, hours=0, minutes=0, 
              seconds=0, args=None, kwargs=None, **options): 
        """
        Schedules a job to be completed _after_ 
        the specified weeks, days, hours, 
        minutes and seconds; starting now.

        func    : name of the callable function
        weeks   : number of weeks to wait
        days    : number of days to wait
        hours   : number of hours to wait
        minutes : number of minutes to wait
        seconds : number of seconds to wait
        args    : arguments to the function 'func'
        """
        alarm_time = datetime.now() + \
                     timedelta(weeks=weeks, days=days, 
                               hours=hours, minutes=minutes, 
                               seconds=seconds)
        return Scheduler.__aps.add_date_job(func, alarm_time, args, options)

    def schedule_after(self, weeks=0, days=0, hours=0, minutes=0, 
                       seconds=0, args=None, kwargs=None, **options): 
        """
        Decorator for Scheduler.after()
        """
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
        """
        Schedules a job to be completed on times
        the matches the given expression.

        func    : name of the callable function
        year    : year to run on
        month   : month to run on
        day     : day of month to run on
        week    : week of the year to run on
        day_of_week: weekday to run on (0 = Monday)
        hour    : hour to run on
        minute  : number of minutes to wait
        second  : second to run on
        start_date: when to first execute the job 
                    and start the counter (default 
                    is after the given interval)
        args    : arguments to the function 'func'
        """
        return Scheduler.__aps.add_cron_job(func, year, month, day, week, 
                                            day_of_week, hour, minute, second, 
                                            start_date, args, options)

    def schedule_cron(self, year='*', month='*', day='*', 
                      week='*', day_of_week='*', hour='*', 
                      minute='*', second='*', start_date=None, 
                      args=None, kwargs=None, **options):
        """
        Decorator for Scheduler.cron()
        """
        def decorator(func):
            func.job = Scheduler.__aps.add_cron_job(func, year, month, day, week, 
                                            day_of_week, hour, minute, second, 
                                            start_date, args, options)
            return func
        return decorator

    def unschedule(self, job=None, func=None, jobid=None):
        """
        Unschedule a given job or function or jobid.
        """
        if job is None and func is None and jobid is None:
            # future compatibility: 
            # TODO: unschedule all the jobs and functions
            #       but for now, just raise an exception
            raise UnSupportedFeature
        elif job is None and func is not None and jobid is None:
            # unschedule the given function in 'func' parameter
            # ignore 'job' and 'jobid' parameters
            Scheduler.__aps.unschedule_func(func)
        elif job is not None and func is None and jobid is None:
            # unschedule the given job in 'job' parameter
            # ignore 'func' and 'jobid' parameters
            Scheduler.__aps.unschedule_job(job)
        elif job is None and func is None and jobid is not None:
            # unschedule the given job in 'jobid' parameter
            # ignore 'func' and 'job' parameters
            # TODO: this feature is expected in APScheduler 3.0
            #       placeholder till then!
            raise UnSupportedFeature
        else:
            # wrong incoming parameter combinations 
            raise UnSupportedParameter
            
    def get_scheduled_jobs(self):
        """
        Returns a list of all scheduled jobs. 
        """
        return Scheduler.__aps.get_jobs()

    def get_scheduled_jobs_list(self):
        """
        Prints the list of all scheduled jobs 
        in human readable format. 
        """
        return Scheduler.__aps.print_jobs()

#
# End of Scheduler Classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Print Help Message when this file is executed
#
if __name__ == '__main__':
    print """    This scheduler provides the following functions 
     [1] at()    : execute func at given date & time 
     [2] every() : execute func every w, d, h, s, m 
     [3] after() : execute func after given date & time 
     [4] cron()  : execute func based on various expressions 
                   on each field - y, m, d, w, dow, h, m, s 

    NOTE:  
     [a] the scheduler provides decorators  
         for all the above mentioned functions. 
     [b] please refer the usage.py for examples
         on how to use the scheduler.

    Thank you!!"""
#
# End 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
