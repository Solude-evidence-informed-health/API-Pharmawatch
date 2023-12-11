IMAGE_NAME = gcr.io/solude-growth/pharmawatch-api:latest
APP_NAME = pharmawatch-api
REGION = southamerica-east1

build:
	docker build -t $(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)

deploy:
	gcloud run deploy $(APP_NAME) \
	  --image $(IMAGE_NAME) \
	  --platform managed \
	  --allow-unauthenticated \
	  --memory 512Mi \
	  --labels key1=pharmawatch,key2=api \
	  --port 80 \
	  --region $(REGION)

build-deploy: build push deploy