
IMAGE_NAME=api-rpi-monitor
IMAGE_VERSION?=$(shell cat version.txt)
BOT_CONTAINER_ALIAS=rpi-monitor-api
PYTHON_INTERPRETER=/bin/python3.11

# Enable experimental functionality in Docker to build for ARM64
export DOCKER_CLI_EXPERIMENTAL = enabled

clean-image:
	-docker rmi `docker images -q --filter=reference=${IMAGE_NAME}:${IMAGE_VERSION}`

clean-image-linux-arm:
	for id in $$(docker images -q ${IMAGE_NAME}:${IMAGE_VERSION}); do \
		if docker image inspect $$id --format '{{.Architecture}}' | grep -q 'arm64'; then \
			docker rmi $$id; \
		fi \
	done

build: clean-image
	docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .

create-builder:
	if ! docker buildx ls | grep -q 'multipatform'; then docker buildx create --use; fi

build-linux-arm: create-builder clean-image-linux-arm
	docker buildx build --load --platform linux/arm64 -t ${IMAGE_NAME}:${IMAGE_VERSION} .

arm-image-export:
	docker save -o $(IMAGE_NAME)_$(IMAGE_VERSION)_ARM64.tar $(IMAGE_NAME):$(IMAGE_VERSION)

arm-send-to-rpi-tokyo: arm-image-export
	scp $(IMAGE_NAME)_$(IMAGE_VERSION)_ARM64.tar rpitokyo:~/; \
	ssh rpitokyo "docker load -i $(IMAGE_NAME)_$(IMAGE_VERSION)_ARM64.tar"; \
	ssh rpitokyo "rm $(IMAGE_NAME)_$(IMAGE_VERSION)_ARM64.tar"

run:
	docker run \
	--name ${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION} \
	-d \
	--security-opt systempaths=unconfined \
	${IMAGE_NAME}:${IMAGE_VERSION}

stop:
	-docker stop `docker ps -q --filter name=${BOT_CONTAINER_ALIAS}`

resume:
	-docker start `docker ps -a -q --filter name=${BOT_CONTAINER_ALIAS}`

remove:
	-docker rm `docker ps -a -q --filter name=${BOT_CONTAINER_ALIAS}`

deploy: build run

redeploy: build stop remove run

logs:
	docker logs -f `docker ps -q --filter name=${BOT_CONTAINER_ALIAS}`

test:
	${PYTHON_INTERPRETER} -m pip install -r requirements.txt
	${PYTHON_INTERPRETER} -m uvicorn app.main:rpi_mon_api --reload

stats:
	docker stats

gittag:
	git tag -a ${IMAGE_VERSION} -m "Release ${IMAGE_VERSION}"
	git push origin ${IMAGE_VERSION}
	@echo "Updating version..."
	@echo "$(shell cat version.txt)-SNAPSHOT" > version.txt
	@echo "Version updated to $(shell cat version.txt)"

gittags:
	git tag --sort version:refname | tail