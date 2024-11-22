# BUILD
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

# NGINX
FROM nginx:latest as prod

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80/tcp


#CMD ["tail", "-f", "/dev/null"]
CMD ["nginx", "-g", "daemon off;"]