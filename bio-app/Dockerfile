# dev just uses the image, volume is created in composer. You need to manually install packages
FROM node:19 as base

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install

# production does not use predifined volume, so needs to copy sorce code
FROM base as prod

COPY . .

RUN npm run build

CMD ["npm", "run", "serve", "--", "--host"]
