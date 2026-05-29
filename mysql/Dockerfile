FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-secret}
ENV MYSQL_DATABASE=${MYSQL_DATABASE:-perritos}

COPY init.sql /docker-entrypoint-initdb.d/init.sql

EXPOSE 3306
