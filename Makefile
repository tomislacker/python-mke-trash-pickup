PYTHON_VERSION := 2
PIP_VERSION := $(PYTHON_VERSION)
VENV_DIR := venv
LDIST_ZIP := $(shell readlink -m mke-trash-pickup.zip)
STACK_NAME := mke-trash-pickup
DEPLOY_BUCKET := mke-trash-pickup-12241
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

.PHONY    : s3-bucket
s3-bucket :
	aws s3 mb s3://$(DEPLOY_BUCKET)

.PHONY           : s3-bucket-delete
s3-bucket-delete :
	aws s3 rm s3://$(DEPLOY_BUCKET) --force

.PHONY    : s3-deploy
s3-deploy :
	aws s3 cp $(LDIST_ZIP) s3://$(DEPLOY_BUCKET)/$(shell basename $(LDIST_ZIP))

.PHONY : cloud
cloud  :
	aws cloudformation create-stack \
		--stack-name $(STACK_NAME) \
		--template-body file://cloudformation.yml \
		--capabilities CAPABILITY_IAM \
		--parameters \
			ParameterKey=DeployBucketName,ParameterValue=$(DEPLOY_BUCKET) \
			ParameterKey=DeployKeyName,ParameterValue=$(shell basename $(LDIST_ZIP)) \
			ParameterKey=LambdaHandler,ParameterValue=$(LAMBDA_HANDLER).lambda_handler \
			ParameterKey=SNSTopicName,ParameterValue=mke-trash-pickup \
			ParameterKey=AddressNumber,ParameterValue=$(ADDRESS_NUM) \
			ParameterKey=AddressDirection,ParameterValue=$(ADDRESS_DIR) \
			ParameterKey=StreetName,ParameterValue=$(STREET_NAME) \
			ParameterKey=StreetType,ParameterValue=$(STREET_TYPE)

.PHONY       : cloud-update
cloud-update :
	aws cloudformation update-stack \
		--stack-name $(STACK_NAME) \
		--template-body file://cloudformation.yml \
		--capabilities CAPABILITY_IAM \
		--parameters \
			ParameterKey=DeployBucketName,ParameterValue=$(DEPLOY_BUCKET) \
			ParameterKey=DeployKeyName,ParameterValue=$(shell basename $(LDIST_ZIP)) \
			ParameterKey=LambdaHandler,ParameterValue=$(LAMBDA_HANDLER).lambda_handler \
			ParameterKey=SNSTopicName,ParameterValue=mke-trash-pickup \
			ParameterKey=AddressNumber,ParameterValue=$(ADDRESS_NUM) \
			ParameterKey=AddressDirection,ParameterValue=$(ADDRESS_DIR) \
			ParameterKey=StreetName,ParameterValue=$(STREET_NAME) \
			ParameterKey=StreetType,ParameterValue=$(STREET_TYPE)

.PHONY       : cloud-delete
cloud-delete :
	aws cloudformation delete-stack \
		--stack-name $(STACK_NAME)
