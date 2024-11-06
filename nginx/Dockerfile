FROM nginx:1.25.1

ARG ENV
ARG SERVER_NAME

COPY ${ENV}.conf.template /etc/nginx/conf.d/nginx.conf.template
COPY uwsgi_params /etc/nginx/uwsgi_params
COPY key/fullchain.pem /etc/letsencrypt/live/${SERVER_NAME}/fullchain.pem
COPY key/privkey.pem /etc/letsencrypt/live/${SERVER_NAME}/privkey.pem

RUN touch /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log
RUN chown nginx:nginx /var/log/ -R