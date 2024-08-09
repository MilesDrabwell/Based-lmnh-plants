# Pipeline

## Folder overview

- This folder contains all the files needed to run the pipeline as a lambda function on AWS.

- This includes the `extract.py` file which retrieves the plant data from the API, `transform.py` which takes this data and transforms it so it's ready to be loaded into the database and `load.py` which uploads the data to the database.

- These files are the combined in `pipeline.py` which runs the entire pipeline as a lambda script.

- Also included is all the terraform necessary to set up the services needed to run the lambda script on AWS every minute.

### Files you need to include

To run the all files in this folder, you need to also include your own `terraform.tfvars` and `.env` files.

These hold private values used to connect to a database and AWS. Both files need these vales - 

```python
AWS_ACCESS_KEY  = # AWS public key
AWS_SECRET_KEY = #AWS secret key
AWS_REGION = #AWS region

DB_HOST = # AWS database endpoint
DB_PORT = # AWS database port
DB_PASSWORD = # AWS database password
DB_NAME = # AWS database name
DB_USER # AWS database username
```

### How to deploy

- Create an AWS ECR (Elastic container registry).

- Also in this folder is a dockerfile, so first you would build an image with this dockerfile and push to the **AWS ECR repository that you created.**
```bash
docker build -t pipeline_lambda . --platform "linux/amd64"

docker tag based_plants:v1.0 <your_ECR_URI>

docker push <your_ECR_URI>
```

- Run `terraform init` then `terraform apply` in the terminal to set up the AWS services which should run the image.