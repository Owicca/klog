run:
	sudo docker run -ti --rm \
		--name klog \
		-v $(shell pwd):/app/ \
		-w /app/ \
		python:latest bash
