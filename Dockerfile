FROM python:3.12-alpine
WORKDIR /opt/triviaserver

RUN apk update && apk add --no-cache socat && apk upgrade && apk cache clean
RUN pip install --no-cache-dir requests

COPY . .

RUN addgroup -S trivia && adduser -S trivia -G trivia
RUN chown -R trivia:trivia /opt/triviaserver
USER trivia

EXPOSE 1337

ENV FLAG=YOUR_FLAG_HERE

CMD ["socat", "-dd", "TCP-LISTEN:1337,fork,reuseaddr", "EXEC:python3 experimentals/adv_telemetry_server.py"]
