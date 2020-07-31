install:
	@poetry install

lint:
	@poetry run flake8 loader

test:
	@poetry run pytest --cov=loader --cov-report xml tests/

public:
	@poetry build
	@poetry config repositories.dist https://test.pypi.org/legacy/
	@poetry publish -r dist









.PHONY : install lint test public
