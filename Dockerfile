FROM docker:dind

EXPOSE 8080

COPY arduino arduino
COPY rpi-pico rpi-pico
COPY main.py .
COPY relay relay
COPY requirements.txt .

RUN apk add --no-cache usbutils python3 py3-pip && \
    pip install -r requirements.txt

CMD ["waitress-serve", "main:app"]