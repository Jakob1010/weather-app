FROM python:3.9.5

# location for scripts
WORKDIR /code
ENV PYTHONPATH=/code/src

# install python requirements
RUN apt-get update && apt-get install cron -y

# install pyhon requeirements
ADD ./containers/pipelinerunner/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy repo
COPY ./ /code/

# copy cron job
COPY src/scheduler/pull_weather_cron /etc/cron.d/pull_weather_cron

# Give execution rights
RUN chmod 777 /etc/cron.d/pull_weather_cron

# Apply cron job
RUN crontab /etc/cron.d/pull_weather_cron

# Log 
RUN touch /var/log/cron.log

# Run cron
CMD cron && tail -f /var/log/cron.log
