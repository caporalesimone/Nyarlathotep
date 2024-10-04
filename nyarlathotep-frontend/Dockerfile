# nyarlathotep-frontend/Dockerfile
FROM node:20.17.0-alpine3.20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . . 

RUN npm run build

CMD ["npm", "run", "preview", "--", "--host"]

EXPOSE 4173