# import the scheduler
from scheduler import Scheduler as scheduler

# to calculate date and time 
from datetime import datetime, timedelta

# inspect is needed to get the function name
import inspect

# this is a common function which is scheduled 
# at many times using many different scheduler 
# functions like at(), every(), after() and cron(). 
def func(args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# create an instance of the scheduler 
sched = scheduler()


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.at() 
#
# input:
#   func : name of the function to be called
#   date : date and time to be called
#   args : arguments to the function 'func'
#
# an at() job executes at 10 seconds from now
j1_time = datetime.now() + timedelta(seconds=10)
at_j1 = sched.at(func, j1_time, args=["AT +10s"])

# an at() job executes at 20 seconds from now
j2_time = datetime.now() + timedelta(seconds=20)
at_j2 = sched.at(func, j2_time, args=["AT +20s"])

# an at() job executes at 30 seconds from now
j3_time = datetime.now() + timedelta(seconds=30)
at_j3 = sched.at(func, j3_time, args=["AT +30s"])

# decorator for at() 
# executes at 15 seconds from now
j4_time = datetime.now() + timedelta(seconds=15)
@sched.schedule_at(date=j4_time, 
                   args=["DECORATOR", "AT", "+15s"])
def dec_at(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())
#
# End of at() 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.every() 
#
# input:
#   func    : name of the function to be called
#   weeks   : number of weeks to wait
#   days    : number of days to wait
#   hours   : number of hours to wait
#   minutes : number of minutes to wait
#   seconds : number of seconds to wait
#   start_date: when to first execute the job 
#               and start the counter 
#               (default is after the given interval)
#   args    : arguments to the function 'func'
#
# executes every 5 seconds starting now 
every_j1 = sched.every(func, args=["EVERY 5s"], seconds=5)

# executes every 10 seconds 
# starting at 90 seconds from now
j2_start_date = datetime.now() + timedelta(seconds=90)
every_j2 = sched.every(func, start_date=j2_start_date, 
                       args=["EVERY 10s"], seconds=10)

# decorator for every()
# executes every 30 seconds starting now
@sched.schedule_every(seconds=30,
                      args=["DECORATOR", "EVERY", "+30s"])
def dec_every(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())
#
# End of every() 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.after() 
#
# input:
#   func    : name of the function to be called
#   weeks   : number of weeks to wait
#   days    : number of days to wait
#   hours   : number of hours to wait
#   minutes : number of minutes to wait
#   seconds : number of seconds to wait
#   args    : arguments to the function 'func'
#
# executes after 45 seconds from now
after_j1 = sched.after(func, seconds=45, 
                       args=["AFTER +45s"])

# executes after 2 minutes 30 seconds from now
j7 = sched.after(func, minutes=2, seconds=30, 
                 args=["AFTER +2m30s"])

#decorator for "after"
@sched.schedule_after(minutes=1, seconds=2,
                      args=["DECORATOR", "AFTER", "+1m2s"])
def dec_after(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())
#
# End of after() 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.cron() 
#
# input:
#   func    : name of the function to be called
#   year    : year to run on
#   month   : month to run on
#   day     : day of month to run on
#   week    : week of the year to run on
#   day_of_week: weekday to run on (0 = Monday)
#   hour    : hour to run on
#   minute  : number of minutes to wait
#   second  : second to run on
#   start_date: when to first execute the job 
#               and start the counter 
#               (default is after the given interval)
#   args    : arguments to the function 'func'
#
# executes at the following:
# year      : 2012, 2013, 2014 and 2015
# months    : jan, feb, march, may, july, sept, nov and dec
# seconds   : every 5 seconds  
cron_j1 = sched.cron(func, year='2012-2015', 
                     month='1-3,5,7,9,11-12', 
                     second='5,10,15,20,25,30,35,40,45,50,55,60', 
                     args=["CORN 5s,m1-3,5,7,9,11,12,y2012-15"])

# decorator for corn()
# executes at the following:
# year      : 2013
# months    : feb, march, apr, may, june and july
# seconds   : every 15 seconds  
@sched.schedule_cron(year='2013', month='2-7', second='15,30,45,60',
                     args=["DECORATOR", "CORN", "15s,m2-7,y2013"])
def dec_cron(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())
#
# End of cron() 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.get_scheduled_jobs() 
# Scheduler.get_scheduled_jobs_list() 
#
# return:
#   get_scheduled_jobs : list of all scheduled jobs
#                        each entry on this list are 
#                        instance of type job 
#
#   get_scheduled_jobs_list : human readable list of 
#                             all scheduled jobs,
#                             returns string.
#
# print the list of all scheduled jobs 
# for every 1 minute
@sched.schedule_every(minutes=1,
                      args=["EVERY", "+1m"])
def dec_print_scheduled_jobs(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, sched.get_scheduled_jobs(), \
          datetime.now())

# print the list of all scheduled jobs in 
# human readable format - for every 45 seconds
@sched.schedule_every(seconds=45,
                      args=["EVERY", "+45s"])
def dec_print_scheduled_jobs_list(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, sched.get_scheduled_jobs_list(), \
          datetime.now())
#
# End of Scheduler.get_scheduled_jobs()
# End of Scheduler.get_scheduled_jobs_list()
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Scheduler.unschedule() 
#
# input:
#   job     : instance of type job to be unscheduled 
#   func    : function - all jobs scheduled on this 
#             function will be unscheduled
#   jobid   : job with jobid will be unscheduled (TODO)
#
# unschedule_func function is called at 3 minutes 
# from now. this function will unschedule all the 
# above scheduled example functions!
unsched_time = datetime.now() + timedelta(minutes=3)
@sched.schedule_at(date=unsched_time, 
                   args=["UNSCHEDULE", "AT", "+3m"])
def unschedule_func(*args):
    fname = inspect.stack()[0][3] #function name
    print '%s : %s : current time "%s"' % \
          (fname, args, datetime.now())
    #sched.unschedule(job=j4)
    #sched.unschedule(jobid=123)
    sched.unschedule(func=func)
    sched.unschedule(func=dec_cron)
    #sched.unschedule(func=dec_after)
    sched.unschedule(func=dec_every)
    #sched.unschedule(func=dec_at)
    sched.unschedule(func=dec_print_scheduled_jobs)
    sched.unschedule(func=dec_print_scheduled_jobs_list)
#
# End of Scheduler.unschedule()
# # # # # # # # # # # # # # # # # # # # # # # # # # # #



# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# start the scheduler
#
print 'This program will run for 3 minutes'
print 'To exit before that, press Ctrl+C'
sched.start()


print '__END__'


