PYTHON_VERSION := 3
PIP_VERSION := $(PYTHON_VERSION)
VENV_DIR := venv


.PHONY: deps

venv:
	virtualenv -p python$(PYTHON_VERSION) $(VENV_DIR)

deps: venv
	$(VENV_DIR)/bin/pip$(PIP_VERSION) install -r requirements.txt
