FROM node:22 as frontend-builder

WORKDIR /app
COPY . .

RUN npm install && npm run build