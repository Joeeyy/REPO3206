FROM library/nginx

RUN apt-get update && \
apt-get install -y php php-fpm 

COPY ./nginx/index.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/www.conf /etc/php/7.3/fpm/pool.d/
COPY ./www/html/index.php /var/www/html/
COPY ./www/html/index.html /var/www/html/
COPY ./start.sh /
COPY ./flag.txt /
COPY ./readflag /
RUN chmod 755 /readflag
RUN chmod 700 /flag.txt

CMD bash /start.sh

EXPOSE 80