# base image는 python:3.9로 시작한다.
FROM python:3.9-alpine

#ENV PYTHONIOENCODING=utf-8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

# install system dependencies
#RUN apt-get update && apt-get install -y netcat-traditional
RUN apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt

#COPY entrypoint.sh
#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
#RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

RUN python manage.py collectstatic --settings=core.settings
RUN chmod -R 755 ./static

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]