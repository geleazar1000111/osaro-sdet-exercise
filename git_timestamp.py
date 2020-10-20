"""Script to commit git files with current time"""

from datetime import datetime
from pytz import timezone
import os
import argparse

format = "%Y-%m-%d %H:%M:%S"

def convert_to_local_time():
    now_utc = datetime.now(timezone('UTC'))
    now_pacific = now_utc.astimezone(timezone('US/Pacific'))
    return now_pacific.strftime(format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Provide timestamp with git commit messages''')
    parser.add_argument('--message', dest="msg", help='Message to include with git commit')
    parser.add_argument('--files', dest="files",nargs='+', help='Files to commit')
    args = parser.parse_args()

    try:
        if not args.files:
            os.system(f'git commit -m "{args.msg} || Timestamp: {convert_to_local_time()}" .')
        else:
            for filename in args.files:
                os.system(f'git commit -m "{args.msg} || Timestamp: {convert_to_local_time()}" ./{filename}')
        os.system("git push origin test-exercise")
        print("Success")
    except Exception as e:
        print(e)