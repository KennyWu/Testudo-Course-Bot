FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY Retrieval ./Retrieval
COPY config.json . 

CMD [ "python3", "./Retrieval/RetrieveBot.py"]