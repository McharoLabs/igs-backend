FROM node:20.10.0-alpine

WORKDIR /client

COPY package.json .

RUN npm install

RUN npm i -g serve

COPY . .


RUN npm run build

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"] 