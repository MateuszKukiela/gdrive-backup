FROM python:3.9.0-buster

# Install cron
RUN apt-get update && apt-get install -y cron

# Add files

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD entrypoint.sh /entrypoint.sh

RUN mkdir -p /credentials

RUN mkdir -p /appdata

RUN chmod +x /run.sh /entrypoint.sh

COPY requirements.txt requirements.txt
COPY backup.py backup.py
COPY restore.py restore.py

RUN pip install -r requirements.txt

ENTRYPOINT /entrypoint.sh

RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
