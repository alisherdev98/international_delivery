FROM nginx:1.21-alpine

# RUN unlink /var/log/nginx/access.log
# RUN unlink /var/log/nginx/error.log

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d