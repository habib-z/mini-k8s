FROM node:20.10.0-alpine3.18
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm i
COPY ./ ./

# EXPOSE 3000
CMD ["npm", "run", "dev"]