PYTHON_VERSION := 2
PIP_VERSION := $(PYTHON_VERSION)
VENV_DIR := venv
LDIST_ZIP := $(shell readlink -m lambda-upload.zip)
LAMBDA_NAME := check-garbage-day
LAMBDA_HANDLER := refusereminder

venv:
	virtualenv -p python$(PYTHON_VERSION) $(VENV_DIR)

.PHONY : deps
deps   : venv
	$(VENV_DIR)/bin/pip$(PIP_VERSION) install -e .

.PHONY : ldist
ldist  : deps
	zip -r $(LDIST_ZIP) $(LAMBDA_HANDLER).py mkerefuse -x *.pyc
	cd $(VENV_DIR)/lib/python2.7/site-packages && zip -r $(LDIST_ZIP) *

.PHONY            : lambda-job-create
lambda-job-create : ldist
	 @echo Uploading $(shell basename $(LDIST_ZIP))
	 @aws lambda create-function \
		 --function-name $(LAMBDA_NAME) \
		 --zip-file fileb://$(LDIST_ZIP) \
		 --handler $(LAMBDA_HANDLER).lambda_handler \
		 --runtime python2.7 \
		 --role arn:aws:iam::097270082659:role/lambdainvoke \
		 --timeout 15 \
		 --memory-size 128

.PHONY            : lambda-job-delete
lambda-job-delete :
	aws lambda delete-function \
		--function-name $(LAMBDA_NAME)

.PHONY            : lambda-job-update
lambda-job-update : ldist
	 @echo Uploading $(SDIST_ZIP)
	 @aws lambda update-function-code \
		 --function-name $(LAMBDA_NAME) \
		 --zip-file fileb://$(LDIST_ZIP)
