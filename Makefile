PYTHON_VERSION := 2
PIP_VERSION := $(PYTHON_VERSION)
VENV_DIR := venv
LDIST_ZIP := $(shell readlink -m lambda-upload.zip)
LAMBDA_NAME := check-garbage-day
LAMBDA_HANDLER := refusereminder

BUILD_CONTAINER_NAME := mke-trash-pickup_libs
BUILD_CONTAINER_IMAGE := amazonlinux:latest


venv:
	virtualenv -p python$(PYTHON_VERSION) $(VENV_DIR)

.PHONY : deps
deps   : venv
	$(VENV_DIR)/bin/pip$(PIP_VERSION) install -e .

site-packages :
	@docker rm -f $(BUILD_CONTAINER_NAME) >&/dev/null || true
	@docker run \
		-id \
		-v $(shell pwd):/code:ro \
		--name $(BUILD_CONTAINER_NAME) \
		$(BUILD_CONTAINER_IMAGE)
	@docker exec -it $(BUILD_CONTAINER_NAME) yum install -y \
		gcc \
		libxml2-devel \
		libxslt-devel \
		python27 \
		python27-devel \
		python27-pip
	@docker exec -it $(BUILD_CONTAINER_NAME) pip install /code
	@docker cp \
		$(BUILD_CONTAINER_NAME):/usr/local/lib64/python2.7/$@ \
		./$@-64
	@docker cp \
		$(BUILD_CONTAINER_NAME):/usr/local/lib/python2.7/$@ \
		./$@
	@docker rm -f $(BUILD_CONTAINER_NAME)

.PHONY : ldist
ldist  : site-packages
	zip -r $(LDIST_ZIP) $(LAMBDA_HANDLER).py mkerefuse -x *.pyc
	cd site-packages-64 && zip -r $(LDIST_ZIP) *
	cd site-packages && zip -r $(LDIST_ZIP) *

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
	 @echo Uploading $(LDIST_ZIP)
	 @aws lambda update-function-code \
		 --function-name $(LAMBDA_NAME) \
		 --zip-file fileb://$(LDIST_ZIP)
