#!/bin/bash
# uwsgiの起動もこのファイルで実行しようとしたが、本番環境でエラーになるためdocker-compose.ymlで実行することにした(2024/05/27)

# 環境変数を読み込む
source /app/.env

# マイグレーションを実行
python3 manage.py migrate --settings=$DJANGO_SETTINGS_MODULE

# コンテナをフォアグラウンドで実行し続けるためにコマンドを追加
exec "$@"
