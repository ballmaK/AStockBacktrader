import time
import datetime

HOUR_SECONDS = 3600
DAY_SECONDS = 86400
DATE_FORMAT_FULL_TO_SECONDS = '%Y%m%d%H%M%S'
DATE_FORMAT_TO_DAY_WITHOUT_DASH = '%Y%m%d'
DATE_FORMAT_TO_DAY = '%Y-%m-%d'
DATE_FORMAT_TO_SECOND = '%H:%M:%S'
DATE_FORMAT_FULL = ' '.join([DATE_FORMAT_TO_DAY, DATE_FORMAT_TO_SECOND])

def reformat_date(date):
    return date.to_pydatetime().strftime(DATE_FORMAT_TO_DAY)
def get_next_day(date):
    if not date:
        date = datetime.datetime.now()
    next_day = date + datetime.timedelta(days=1)
    return next_day

def get_nextN_day(date, n):
    if not date:
        date = datetime.datetime.now()
    next_day = date + datetime.timedelta(days=n)
    return next_day

def get_today_timestamp():
    return time.mktime(time.strptime(time.strftime(DATE_FORMAT_TO_DAY, time.localtime(time.time())), DATE_FORMAT_TO_DAY))

def get_datetime_str_for_now():
    return time.strftime(DATE_FORMAT_FULL_TO_SECONDS, time.localtime(time.time()))

def get_current_day_delay_seconds(delay_seconds):
    current_timestamp = time.mktime(time.strptime(time.ctime()))
    current_date_format_str = time.strftime(DATE_FORMAT_TO_DAY, time.localtime(current_timestamp))
    current_date_timestamp = time.mktime(time.strptime(current_date_format_str, DATE_FORMAT_TO_DAY))
    return current_date_timestamp + delay_seconds

def get_nextNDay(current_timestamp, n):
    date_N_days_ago = current_timestamp + DAY_SECONDS * n
    x = time.strftime(DATE_FORMAT_TO_DAY, time.localtime(date_N_days_ago))
    return x

def earlyThan(target_timestamp):
    return time.mktime(time.strptime(time.ctime())) < target_timestamp

def getDaysBetween(start_date, end_date):
    start_timestamp = time.mktime(time.strptime(start_date, DATE_FORMAT_TO_DAY))
    end_timestamp = time.mktime(time.strptime(end_date, DATE_FORMAT_TO_DAY))
    return (end_timestamp - start_timestamp) / DAY_SECONDS

if __name__ == '__main__':
    # print(DATE_FORMAT_FULL)
    # print(time.strftime(DATE_FORMAT_FULL, time.localtime(getCurrentDayDelaySeconds(3600 * 17))))

    print(getDaysBetween('2021-02-20', '2021-03-05'))