FROM python:3

COPY server.py ./
COPY Makefile ./
COPY Dockerfile ./
COPY readme.md ./
COPY var ./

EXPOSE 65430
ENTRYPOINT ["python3", "server.py"]
