help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "    install   to install the dependencies, including the development ones"
	@echo "    format    to format the code"
	@echo "    lint      to lint the code"
	@echo "    test      to run the tests"
	@echo "    test-report to run the tests and generate a report"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

format:
	python -m black .

lint:
	python -m mypy .
	python -m flake8 .

test:
	python scripts/test.py

test-report:
	python scripts/test.py --report

clean:
	python scripts/clean.py
