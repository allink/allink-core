# These targets are not files
.PHONY: help clean docs release 
.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs: ## mkdocs served on localhost
	mkdocs serve

tag: clean ## create a new tag and push on git
	python setup.py tag

publish: clean ## package and upload a release
	python setup.py publish
	twine upload dist/*

test-publish: clean ## package and upload a release
	python setup.py publish
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*