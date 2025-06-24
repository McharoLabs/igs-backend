FROM node:20.19.2-alpine

WORKDIR /client

COPY package.json .

RUN npm install --timeout=60000

RUN npm i -g serve

COPY . .


RUN npm run build

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"] 