FROM nginx:latest

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /nginx_files /tmp/upload_tmp && \
    chmod -R 777 /nginx_files /tmp/upload_tmp

#VOLUME /nginx_files

#EXPOSE 8081

CMD ["nginx", "-g", "daemon off;"]