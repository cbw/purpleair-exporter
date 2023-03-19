DOCKER_USERNAME ?= chrisbwilson
APPLICATION_NAME ?= purpleair-exporter
GIT_HASH ?= $(shell git log --format="%h" -n 1)
RELEASE_VERSION ?= $(shell scripts/version.sh)

build:
	docker buildx build --push --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --tag ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} .
 
push:
	docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}

release:
	docker pull ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}
	docker tag  ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest
	docker tag  ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} ${DOCKER_USERNAME}/${APPLICATION_NAME}:${RELEASE_VERSION}
	docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest