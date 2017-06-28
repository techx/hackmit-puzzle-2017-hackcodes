FROM mhart/alpine-node:6

ARG APP_PATH=/hackcodes

RUN apk add --update --no-cache python3 python3-dev build-base linux-headers
RUN pip3 install --upgrade pip

RUN pip3 install uwsgi gevent
#RUN CFLAGS="$CFLAGS -L/lib" pip3 install uwsgi

WORKDIR $APP_PATH

COPY requirements.txt $APP_PATH
RUN pip3 install -r requirements.txt

COPY package.json $APP_PATH
RUN npm install
RUN npm install -g webpack

COPY . $APP_PATH

RUN webpack

EXPOSE 8000
CMD ["uwsgi", "--static-map", "/static=static", "--gevent", "100", "--gevent-monkey-patch", "--http", ":8000", "--wsgi-file", "app.py", "--callable", "app"]
