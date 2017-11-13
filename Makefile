first:

pep8:
	find . -name '*.py' -exec pep8 --ignore=E501 -r {} \;

flake8:
	flake8 --ignore=E501

unit-test:
	python -m unittest discover -v tests/ '*_test.py'

isort:
	isort --recursive .

clean-pyc:
	find . -name '*.pyc' -exec rm -v {} \;
	find . -name '__pycache__' -exec rmdir {} \;
