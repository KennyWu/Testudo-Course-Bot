FROM python:3.8

WORKDIR /app

COPY requirments.txt ./
RUN pip3 install -r requirments.txt

COPY /Retrieval ./

CMD [ "python3", "./Retrieval/RetrieveBot.py"]