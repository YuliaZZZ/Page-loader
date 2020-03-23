install:
	@poetry install

lint:
	@poetry run flake8 gen_diff

test:
	@poetry run pytest --cov --cov-report xml tests/

public:
	@poetry build
	@poetry config repositories.dist https://test.pypi.org/legacy/
	@poetry publish -r dist














.PHONY : lint install test public
