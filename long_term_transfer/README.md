# Long-term transfer

### Folder overview

- This folder contains all the files needed for the upload and deletion of long term data from the database.

- This includes the lambda script for the AWS Lambda function which uploads the previous days data to an s3 bucket and deletes the same data from the database.

- Also included is all the terraform necessary to deploy to the cloud, the terraform creates the lambda function and schedule on AWS, where the schedule should trigger the lambda function at midnight every day.

### How to deploy

- Create an AWS ECR (Elastic container registry).

- Also in this folder is a dockerfile, so first you would build an image with this dockerfile and push to the **AWS ECR repository that you created.**
```bash
docker build -t long_term_transfer_lambda . --platform "linux/amd64"

docker tag based_plants:v1.0 <your_ECR_URI>

docker push <your_ECR_URI>
```

- Run `terraform init` then `terraform apply` in the terminal to set up the AWS services which should run the image.