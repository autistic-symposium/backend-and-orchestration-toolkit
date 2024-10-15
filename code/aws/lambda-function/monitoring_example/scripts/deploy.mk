SAM_INPUT_TEMPLATE=./src/template.yaml
SAM_OUTPUT_TEMPLATE=./src/packaged-template.yaml

.PHONY: validate-env
validate-env:
	@./scripts/validate-env.sh \
	AWS_ACCESS_KEY_ID \
	AWS_REGION \
	AWS_SECRET_ACCESS_KEY \
	STACK_NAME \
	S3_BUCKET

.PHONY: package
package: validate-env
	@aws cloudformation package \
	--template-file ${SAM_INPUT_TEMPLATE} \
	--output-template-file ${SAM_OUTPUT_TEMPLATE} \
	--s3-bucket ${S3_BUCKET} \
	--region ${AWS_REGION}

.PHONY: deploy
deploy: validate-env package
	aws cloudformation deploy \
		--template-file ${SAM_OUTPUT_TEMPLATE} \
		--stack-name ${SAM_STACK_NAME} \
		--capabilities CAPABILITY_IAM \
		--region ${AWS_REGION}

.PHONY: all
all: deploy