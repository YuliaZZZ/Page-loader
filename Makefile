install:
	@poetry install

lint:
	@poetry run flake8 loader

test:
	@poetry run pytest --cov --cov-report xml --disable-warnings tests/

public:
	@poetry build
	@poetry config repositories.dist https://test.pypi.org/legacy/
	@poetry publish -r dist














.PHONY : install lint test public
