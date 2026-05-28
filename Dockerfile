# Modified by @Shadowedtomb and @Hail_Arka

FROM python:3.10.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir "/Shadowd TombBotz"
WORKDIR "/Shadowd TombBotz"
COPY . "/Shadowd TombBotz"
CMD ["python", "bot.py"]

