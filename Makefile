black_formatter:
	poetry run black ./app/ --config pyproject.toml

black_check:
	poetry run black ./app/ --config pyproject.toml --check

isort_formatter:
	poetry run isort ./app/ --settings-path pyproject.toml

isort_check:
	poetry run isort check ./app/ --settings-path pyproject.toml

ruff_checker:
	poetry run ruff check ./app/ --config pyproject.toml

ruff_fix:
	poetry run ruff check ./app/ --config pyproject.toml --fix

run_formaters: black_formatter isort_formatter
run_linters: black_check isort_check ruff_checker

up_compose_local:
	docker compose up -d --build

down_compose_local:
	docker compose down -v
