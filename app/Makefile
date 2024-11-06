#################################
# local環境
#################################

# migration
makemigrations:
	python3 src/manage.py makemigrations --settings src.config.settings.local

migrate:
	python3 src/manage.py migrate --settings src.config.settings.local

# schema生成
yml-schema-generate:
	python3 src/manage.py spectacular --settings src.config.settings.local --color --file docs/schema.yml

json-schema-generate:
	python3 src/manage.py spectacular --settings src.config.settings.local --color --file docs/schema.json --format openapi-json

# ER図生成
erd-generate:
	python3 src/manage.py generate_puml --settings src.config.settings.local --add-help --add-choices --add-legend  --file docs/er.puml

# python3 src/manage.py generate_puml --settings src.config.settings.local --title "AIon 採用DXアシスタント" --add-help --add-choices --add-legend

