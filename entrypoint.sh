#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

# Setup a cron schedule
echo $REMAIN > /REMAIN.txt
echo $TEAM_ID > /TEAM_ID.txt
echo "$CRON /usr/local/bin/python3 /backup.py >> /proc/1/fd/1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron -f
