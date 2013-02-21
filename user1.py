from scheduler import Scheduler as scheduler
from datetime import datetime, date, time, timedelta
import time
import logging

logging.basicConfig(filename='/tmp/log', level=logging.DEBUG,
        format='[%(asctime)s]: %(levelname)s : %(message)s')

class Failed(Exception):
    def __str__(self):
        return 'Failed!!'

class Test:
    def __init__(self, *args, **kwargs):
        self.scheduler = scheduler()
        self.__running = False
        # Intentionally don't want to start!!
        self.__dont_start = True 
        self.__retry_count = 0
        self.__start_max_retries = 5
        self.__retry_timeout = 5 #seconds
        self.__data_transfer_job = None
        self.__data_transfer_timeout = 15 #seconds
    def start(self):
        try:
            # Try to start here! 
            # Intentionally don't wanr to start for the first 5 times
            if self.__retry_count < self.__start_max_retries:
                self.__retry_count += 1
                raise Failed
            if self.__running:
                raise Failed
            self.__running = True
            print 'started successfully :)'
            # initiate data transfer once in self.__data_transfer_timeout
            self.__data_transfer_job = self.scheduler.every(self.transfer, 
                                            seconds=self.__data_transfer_timeout)
            self.scheduler.start()
        except Failed:
            # log the start failure and reschedule the start()
            print 'attempt (#%d): unable to start now.. ' \
                  'so rescheduling to start after %d seconds' % \
                  (self.__retry_count, self.__retry_timeout)
            alarm_time = datetime.now() + \
                         timedelta(seconds=self.__retry_timeout)
            self.scheduler.at(self.start, alarm_time)
            self.scheduler.start()
    def stop(self):
        if self.__running:
            self.__running = False
            self.scheduler.unschedule(job=self.__data_transfer_job)
            if self.scheduler.is_running():
                self.scheduler.stop()
            print 'Good bye!!'
    def transfer(self):
        print 'Data transfer starting now.. ', datetime.now()
        time.sleep(2) # sleep for 2 seconds
        print 'Data transfer done! ', datetime.now()


if __name__ == '__main__':
    t = Test()
    t.start()
        
    # wait for 5 minute
    time.sleep(60)

    t.stop()

