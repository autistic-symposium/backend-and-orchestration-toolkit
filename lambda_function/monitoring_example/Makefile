BASEDIR := "$(PWD)/src"

CMD := docker run -it --rm \
	--volume "/var/run/docker.sock:/var/run/docker.sock" \
	--volume "$(PWD)/src:/var/opt" \
	--volume ~/.aws:/root/.aws \
	--env-file .env 

AWS_REGION := $(shell aws configure get region)

.PHONY: help
help:
	@$(CMD)

.PHONY: build
build:
	@$(CMD) build

.PHONY: validate
validate:
	@$(CMD) validate

.PHONY: local
local:
	@$(CMD) local invoke "MonitoringTest" \
		-t "/var/opt/template.yaml" \
		-e "/var/opt/event.json" \
		--profile "$(AWS_PROFILE)" \
		--docker-volume-basedir "$(BASEDIR)"

.PHONY: logs
logs:
	@$(CMD) logs -n MonitoringTest --stack-name ${STACK_NAME} -t --region ${AWS_REGION} --profile ${AWS_PROFILE}

.PHONY: package
package:
	@$(CMD) package --template-file ./template.yaml --output-template-file ./packaged-template.yaml --s3-bucket ${S3_BUCKET} --region ${AWS_REGION} --profile ${AWS_PROFILE}