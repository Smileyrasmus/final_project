# base used for development
FROM node:19 as base

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install

CMD ["npm", "run", "dev", "--", "--host"]

# prod used for what we call production
FROM base as prod

COPY . .

RUN npm run build

CMD ["npm", "run", "serve", "--", "--host"]
