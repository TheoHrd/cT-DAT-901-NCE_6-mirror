# BUILD
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm

RUN pnpm install --frozen-lockfile --prod

COPY . .

RUN pnpm run build

# NGINX
FROM nginx:latest as prod

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80/tcp


#CMD ["tail", "-f", "/dev/null"]
CMD ["nginx", "-g", "daemon off;"]