FROM alpine:latest
COPY . /app
WORKDIR $HOME/app

ENV API_ENDPOINT "http://172.19.0.2:5000"

RUN apk update
RUN apk add python3 py3-pip
RUN pip3 install -r requirements.txt

EXPOSE 5001

CMD ["python3","front.py"]
