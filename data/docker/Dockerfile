FROM kuralabs/python3-dev:latest
LABEL mantainer="info@kuralabs.io"


# -----

USER root
ENV DEBIAN_FRONTEND noninteractive


# Install supervisord
RUN apt-get update && apt-get install --yes \
        apt-transport-https \
        supervisor dirmngr \
    && rm -rf /var/lib/apt/lists/*


# Install MySQL
RUN echo 'mysql-server-5.7 mysql-server/root_password_again password defaultrootpwd' | debconf-set-selections \
    && echo 'mysql-server-5.7 mysql-server/root_password password defaultrootpwd' | debconf-set-selections \
    && apt-get update && apt-get install --yes \
        mysql-server-5.7 \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/lib/mysql /var/run/mysqld /var/mysqld/ \
    && chown mysql:mysql /var/lib/mysql /var/run/mysqld /var/mysqld/


# Install mongodb
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5 \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb.list \
    && apt-get update && apt-get install --yes \
        mongodb-org \
    && rm -rf /var/lib/apt/lists/*


# Install supervisord configuration and entrypoint script
COPY supervisord/*.conf /etc/supervisor/conf.d/
COPY entrypoint.sh /usr/local/bin/

USER python3
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
