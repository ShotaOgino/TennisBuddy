FROM ubuntu:20.04
USER root

RUN apt update
RUN apt install -y python3.9
RUN apt install -y python3-pip

RUN apt-get update && apt-get install -y python3-dev

#copy requirements.txt .
#RUN python3.9 -m pip install -r requirements.txt

ENV SITE_DOMAIN=tennis-buddy.com

WORKDIR /var

ADD https://atmarkit.itmedia.co.jp/ait/articles/2206/13/news032.html .


#copy script.python3
#ENTRYPOINT ["python3.9", "script.py"]