FROM python:3.11
ARG ENV
ARG DJANGO_USER

# 標準出力・標準エラーのストリームのバッファリングを無効化
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        pkg-config \
        libmariadb-dev \
        clang \
        build-essential \
        postgresql-client

COPY ./requirements.txt ./

RUN addgroup --system django && adduser --system django --ingroup django
RUN addgroup --system nginx && adduser --system nginx --ingroup nginx

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# uwsgiのログファイルを作成
RUN mkdir -p /var/log/uwsgi
RUN touch /var/log/uwsgi/uwsgi.log
RUN chown -R nginx:nginx /var/log/uwsgi/uwsgi.log

# /run/django ディレクトリの作成とパーミッションの設定
RUN mkdir -p /run/django
RUN chown -R nginx:nginx /run/django

COPY ./src /app

RUN chown -R nginx:nginx /app

RUN mkdir /var/log/django
RUN touch /var/log/django/django.log
RUN chown nginx:nginx /var/log/ -R

# COPY certs/ap-northeast-1-bundle.pem /app/certs/
# RUN chmod 644 /app/certs/ap-northeast-1-bundle.pem

# entrypoint.shの実行権限を変更
RUN chmod +x /app/entrypoint.sh

# 本番環境 nginx
# 開発環境 root
# TODO: 開発環境でもnginxにしていたが、db.sqlite3の書き込み権限の問題で開発環境ではrootで起動することにした
# USERを切り替える以外にも方法はあるので、後程変更予定
USER $DJANGO_USER
