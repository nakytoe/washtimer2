# dev environment

FROM python:3.11.4-bullseye

USER root
RUN mkdir /app
COPY . /app
WORKDIR /app

RUN python -m pip install numpy pandas requests

ENV PYTHONPATH /app

ENTRYPOINT ["/bin/bash"]