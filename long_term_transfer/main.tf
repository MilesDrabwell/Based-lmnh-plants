provider "aws" {
  region = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}

resource "aws_lambda_function" "historic_lambda" {
  architectures                      = ["x86_64"]
  function_name                      = "c12-based-update-historic-data"
  image_uri                          = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-lambda:latest"
  layers                             = []
  memory_size                        = 128
  package_type                       = "Image"
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::129033205317:role/service-role/based-update-historic-data-role-nh0kc4vk"
  skip_destroy                       = false
  tags                               = {}
  tags_all                           = {}
  timeout                            = 120
  environment {
    variables = {
      DB_HOST     = var.DB_HOST
      DB_NAME     = var.DB_NAME
      DB_PASSWORD = var.DB_PASSWORD
      DB_PORT     = var.DB_PORT
      DB_USER     = var.DB_USER
    }
  }
  ephemeral_storage {
    size = 512
  }
  logging_config {
    log_format            = "Text"
    log_group             = "/aws/lambda/based-update-historic-data"
  }
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_scheduler_schedule" "lambda_schedule" {
  group_name                   = "default"
  name                         = "c12-based-historic-data-upload"
  schedule_expression          = "cron(0 0 * * ? *)"
  schedule_expression_timezone = "UTC"
  state                        = "ENABLED"
  flexible_time_window {
    maximum_window_in_minutes = 15
    mode                      = "FLEXIBLE"
  }
  target {
    arn      = "arn:aws:lambda:eu-west-2:129033205317:function:c12-based-update-historic-data"
    role_arn = "arn:aws:iam::129033205317:role/service-role/Amazon_EventBridge_Scheduler_LAMBDA_ea33825b28"
    retry_policy {
      maximum_event_age_in_seconds = 86400
      maximum_retry_attempts       = 185
    }
  }
}