FROM node:12.11.1-alpine AS builder

COPY package.json .
COPY yarn.lock .
RUN yarn install

COPY . .

ARG REACT_APP_API_BASE_URL
RUN yarn build

FROM nginx:1.16.1-alpine
COPY --from=builder build /usr/share/nginx/html
