FROM python:3.8
# Install packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y python3-pip apt-utils python3-dev default-libmysqlclient-dev build-essential python3-mysqldb && \
    rm -rf /var/lib/apt/lists/* && rm -fr /var/cache/apt/archives/*
# install the pipenv virtual env
RUN pip3 install gunicorn flask==2.0.2 mysqlclient flask-migrate==2.6.0 flask-script==2.0.5 flask-sqlalchemy flask-login flask_bcrypt flask-restful
# change the working directory
WORKDIR /app
# copy the current project
COPY . .
# expose the port
EXPOSE 3000
# set env variable
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
ENV FLASK_APP=routes.py
# run the command
CMD echo "MYSQL_HOST=$MYSQL_HOST" | tee -a /etc/environment && \
    echo "MYSQL_USERNAME=$MYSQL_USERNAME" | tee -a /etc/environment && \
    echo "MYSQL_PASSWORD=$MYSQL_PASSWORD" | tee -a /etc/environment && \
    echo "MYSQL_DATABASE=$MYSQL_DATABASE" | tee -a /etc/environment && \
    echo "DEBUG=$DEBUG" | tee -a /etc/environment && \
    echo "FLASK_ENV=$FLASK_ENV" | tee -a /etc/environment && \
    echo "FLASK_APP=$FLASK_APP" | tee -a /etc/environment && \
    cd app && \
    gunicorn \
      --timeout 300 \
      --workers 8 \
      --bind 0.0.0.0:3000 \
      routes:app
