dockerbuild:
	docker build -t python-boilerplate:latest .

dockerrun:
	docker run --rm python-boilerplate:latest
