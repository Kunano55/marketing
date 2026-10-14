FROM php:8.2-apache

# Install PDO MySQL extension, OpenSSL, CA certificates and enable Apache modules
RUN apt-get update && apt-get install -y ca-certificates openssl \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-install pdo pdo_mysql \
    && a2enmod rewrite headers

# Copy application files
COPY . /var/www/html/

# Set Apache DocumentRoot and permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Expose HTTP port
EXPOSE 80

CMD ["apache2-foreground"]
