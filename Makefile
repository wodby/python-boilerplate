dockerbuild:
	docker build \
		--build-arg WODBY_BASE_IMAGE=wodby/python:3.14 \
		--build-arg COPY_FROM=. \
		-t python-boilerplate:latest .

dockerrun:
	docker run --rm -p 8080:8080 python-boilerplate:latest
