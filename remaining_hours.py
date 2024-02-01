import sys
from datetime import timedelta
import datetime
import argparse
from pytz import timezone

parser = argparse.ArgumentParser()

# Input arguments
parser.add_argument("-cl", "--colorama", dest = "colorama", help="Use Colorama library; It is necessary to install it", action='store_true', default=False)
parser.add_argument("-tz", "--timezone", dest = "timezone", help="Timezone identifier https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
parser.add_argument("-hw", "--hoursworked", dest = "hours_worked", help="Input hours worked in [HH:MM] format", default=None)
parser.add_argument("-br", "--break", dest = "break_time", help="Input time of end of break in [HH:MM] format", default=None)
parser.add_argument("-hn", "--hoursnecessary", dest = "hours_necessary", help="Amount of time needed to end work [HH:MM] format, default is 8 hours", default='8:00')

# Printing arguments
parser.add_argument("-fb", "--frombreak", dest = "frombreak", help="Print how much time until you're free from break in [HH:MM] format", action='store_true', default=False)
parser.add_argument("-fn", "--fromnow", dest = "fromnow", help="Print when you're free from now in [HH:MM] format", action='store_true', default=False)
parser.add_argument("-at", "--attime", dest = "attime", help="Print at what time you're free in [HH:MM] format", action='store_true', default=False)

args = parser.parse_args()

colorama_BRI = ""
colorama_RES = ""
colorama_DIM = ""
if(args.colorama):
    from colorama import init as colorama_init
    from colorama import Fore, Back
    from colorama import Style
    colorama_init()
    colorama_BRI = f"{Style.BRIGHT}"
    colorama_RES = f"{Style.RESET_ALL}"
    colorama_DIM = f"{Style.DIM}"

# Assigning variables, if arguments were used
try:
    if(args.hours_worked): a, b = args.hours_worked.split(':')
    else:
        ab_list = input('Enter duration of time worked before break [HH:MM]: ').split(':')
        a, b = int(ab_list[0]), int(ab_list[1])
    
    if(args.break_time): c, d = args.break_time.split(':')
    else:
        cd_list = input('Enter end of break [HH:MM]: ').split(':')
        c, d = int(cd_list[0]), int(cd_list[1])
    if(args.hours_necessary): e, f = args.hours_necessary.split(':')
except ValueError as err:
        sys.exit(f"An error occurred. Please use the format in hours and minutes [HH:MM] ({err})")

# Assigning and calculating time
hours_worked = timedelta(hours=int(a),minutes=int(b))
hours_required = timedelta(hours=int(e), minutes=int(f))
break_time = timedelta(hours=int(c),minutes=int(d))
if (args.timezone): time_now = datetime.datetime.now(timezone(args.timezone))
else: time_now = datetime.datetime.now()
time_now_delta = timedelta(hours=time_now.hour,minutes=time_now.minute)
work_delta = break_time + hours_required - hours_worked - time_now_delta # Time until completing work


# Final printing
if work_delta.days<0: # less than 0 time = work done
    print('Work day complete!')
elif (args.frombreak or args.fromnow or args.attime): # if arguments for time are used, they disable the long print-out. They are printed in order of: 1.fb 2.fn 3.at if more are printed
     if args.frombreak: print(f"{':'.join(str(hours_required-hours_worked).split(':')[:2])}")
     if args.fromnow:   print(f"{':'.join(str(work_delta).split(':')[:2])}")
     if args.attime:    print(f"{(time_now + work_delta).strftime('%H:%M')}")
else: 
    print(f"{colorama_BRI}Your work will end at {(time_now + work_delta).strftime('%H:%M')}{colorama_RES}{colorama_DIM}, {':'.join(str(work_delta).split(':')[:2])} h away from now, {':'.join(str(hours_required-hours_worked).split(':')[:2])} h from end of break")
