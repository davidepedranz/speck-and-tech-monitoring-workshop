FROM alpine:3.10.2

RUN apk add --no-cache curl jq
COPY bot.sh /

ENTRYPOINT ["sh", "bot.sh"]
