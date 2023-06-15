FROM alpine:3.18

EXPOSE 8080

COPY arduino arduino
COPY rpi-pico rpi-pico
COPY main.py .
COPY relay relay
COPY requirements.txt .

RUN apk add --no-cache python3 py3-pip && pip install -r requirements.txt

CMD ["waitress-serve", "main:app"]