FROM python:3.8

WORKDIR /app

COPY Retrieval/ ./

RUN pip3 install -r requests beautifulsoup4 discord.py

CMD [ "Python3", "./Retrieval/RetrieveBot.py"]