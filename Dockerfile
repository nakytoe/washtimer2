# replicate aws lambda environment

FROM amazonlinux:2023

RUN dnf install -y git pip python3.11

USER root
RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH /app

ENTRYPOINT ["/bin/bash"]