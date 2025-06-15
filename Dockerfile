FROM php:7.3-fpm
RUN apt-get update && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*
COPY docker/nginx.conf /etc/nginx/nginx.conf
WORKDIR /var/www/html
COPY . .
EXPOSE 80
CMD service nginx start && php-fpm
