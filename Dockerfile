# pull official base image
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update jpeg-dev
# install psycopg2 dependencies
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev zlib zlib-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt . 
RUN pip install -r requirements.txt

# set work directory
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# RUN adduser -D user           # permission problems if create user 
# RUN chown -R user:user /vol/  # 
# RUN chmod -R 755 /vol/web
# USER user

# copy entrypoint.sh
# COPY entrypoint.sh .

# RUN sed -i 's/\r$//g' entrypoint.sh
# RUN chmod +x entrypoint.sh

# copy project
# COPY . .

# run entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]