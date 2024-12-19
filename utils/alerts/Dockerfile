FROM python:3.12-slim

WORKDIR /app

COPY entry.sh /app/entry.sh

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY /src /app/src

CMD [ "bash", "entry.sh" ]
