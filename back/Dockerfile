FROM alpine:latest
COPY . /app
WORKDIR $HOME/app

ENV DB_ENDPOINT "db" 

RUN apk update
RUN apk add python3 py3-pip sqlite
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3","back.py"]
