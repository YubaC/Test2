help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "    help        to show this message"
	@echo "    clean       to clean the project, removing the cache and the reports"
	@echo "    format      to format the code"
	@echo "    install     to install the dependencies, including the development ones"
	@echo "    lint        to lint the code"
	@echo "    setup       to set up the virtual environment, and install the dependencies"
	@echo "    test        to run the tests"
	@echo "    test-report to run the tests and generate a report"

PYTHON = python3
ifeq ($(OS),Windows_NT)
	PYTHON = python
endif

setup:
	$(PYTHON) scripts/setup_env.py

install:
	$(PYTHON) -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

format:
	@$(PYTHON) -m black .

lint:
	@$(PYTHON) -m mypy .
	@$(PYTHON) -m flake8 .

test:
	@$(PYTHON) scripts/test.py

test-report:
	@$(PYTHON) scripts/test.py --report

clean:
	@$(PYTHON) scripts/clean.py
