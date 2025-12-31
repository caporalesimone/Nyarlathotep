# nyarlathotep-frontend/Dockerfile
FROM node:20.17.0-alpine3.20

WORKDIR /app

COPY nyarlathotep-frontend/package*.json .

RUN npm install

COPY nyarlathotep-frontend/. . 

RUN npm run build

CMD ["npm", "run", "preview", "--", "--host"]

EXPOSE 4173