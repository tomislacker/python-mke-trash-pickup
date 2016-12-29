PYTHON_VERSION := 2
PIP_VERSION := $(PYTHON_VERSION)
VENV_DIR := venv
LDIST_ZIP := $(shell readlink -m mke-trash-pickup.zip)
STACK_NAME := mke-trash-pickup
DEPLOY_BUCKET := mke-trash-pickup-12241
LAMBDA_NAME := check-garbage-day
LAMBDA_HANDLER := refusereminder
LAMBDA_FREQ := 12 hours


venv:
	virtualenv -p python$(PYTHON_VERSION) $(VENV_DIR)

.PHONY : deps
deps   : venv
	$(VENV_DIR)/bin/pip$(PIP_VERSION) install -e .

.travis.yml : venv
	@$(VENV_DIR)/bin/pip$(PIP_VERSION) install --quiet tox
	@$(VENV_DIR)/bin/python make_travisyml.py > $@

.PHONY  : version
version : venv
	@echo "import mkerefuse; print(mkerefuse.__version__)" | $(VENV_DIR)/bin/python

.PHONY : ldist
ldist  :
	zip -r $(LDIST_ZIP) $(LAMBDA_HANDLER).py mkerefuse -x *.pyc
	cd $(VENV_DIR)/lib/python2.7/site-packages \
		; zip -r $(LDIST_ZIP) \
			requests \
			-x *.pyc

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
			ParameterKey=StreetType,ParameterValue=$(STREET_TYPE) \
			ParameterKey=Frequency,ParameterValue='$(LAMBDA_FREQ)'

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
			ParameterKey=StreetType,ParameterValue=$(STREET_TYPE) \
			ParameterKey=Frequency,ParameterValue='$(LAMBDA_FREQ)'

.PHONY       : cloud-delete
cloud-delete :
	aws cloudformation delete-stack \
		--stack-name $(STACK_NAME)
