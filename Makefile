install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-remove:
	python3 -m pip uninstall work-with-api

lint:
	poetry run flake8 exercises

test:
	poetry run pytest