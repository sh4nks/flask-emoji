.PHONY: lint clean clean-pyc clean-build docs release develop test

help:
	    @echo "  clean       remove unwanted stuff"
	    @echo "  release     package and upload a release"
	    @echo "  lint        checks for pep8 errors"
	    @echo "  develop     make a development package"
	    @echo "  release     release package on PyPI"
	    @echo "  test        run the tests"

lint:
	@which flake8 || pip install flake8
	@flake8 flask_emoji tests

clean: clean-build clean-pyc clean-docs
	    @find . -name '.DS_Store' -exec rm -f {} +

clean-build:
	    @rm -fr build/
	    @rm -fr dist/
	    @rm -fr *.egg-info
	    @rm -fr cover/

clean-pyc:
	    @find . -name '*.pyc' -exec rm -f {} +
	    @find . -name '*.pyo' -exec rm -f {} +
	    @find . -name '*~' -exec rm -f {} +
	    @find . -name '__pycache__' -exec rm -fr {} +

clean-docs:
	    @rm -fr  docs/_build

docs:
	    @$(MAKE) -C docs html

release:
	    @twine upload dist/*.tar.gz
	    @twine upload dist/*.whl

develop:
	    python setup.py develop

test:
	    py.test
