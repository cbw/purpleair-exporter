DOCKER_USERNAME ?= chrisbwilson
APPLICATION_NAME ?= purpleair-exporter
GIT_HASH ?= $(shell git log --format="%h" -n 1)

build:
         docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64 --tag ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} .
 
push:
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}

release:
         docker pull ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}
         docker tag  ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest